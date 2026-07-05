import os
import torch
from transformers import Trainer
import torch.nn.functional as F


def fill_active_segments(active_score: torch.Tensor) -> torch.Tensor:
    """
    Fill each non-zero score in `active_score` forward until the next non-zero score.
    Example:
        [0, 0, 0.8, 0, 0, 0.6, 0] → [0, 0, 0.8, 0.8, 0.8, 0.6, 0.6]
    Supported shape: [B, T, 1]
    """
    assert active_score.ndim == 3 and active_score.size(-1) == 1
    B, T, _ = active_score.shape
    x = active_score.squeeze(-1)  # [B, T]

    # 1. Build anchor mask
    anchors = (x != 0).float()               # [B, T]

    # 2. Build index of the nearest previous anchor for each position
    idx = torch.arange(T, device=x.device).unsqueeze(0).expand(B, T)  # [B, T]
    anchor_idx = idx * anchors                                               # Non-zero positions = index, others = 0
    filled_idx = torch.cummax(anchor_idx, dim=1)[0]                          # Forward-propagate the last non-zero index

    # 3. Gather corresponding anchor values
    filled = x.gather(1, filled_idx.long())                                  # [B, T]

    # 4. The initial region before the first non-zero should remain 0
    first_anchor_seen = anchors.cumsum(dim=1) > 0
    filled = filled * first_anchor_seen.float()

    return filled.unsqueeze(-1)                                              # [B, T, 1]

class ProActTrainer(Trainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute_active_loss(self, active_logits, active_labels):
        """
        active_logits: (B, T, 1)
        active_labels: (B, T), values are {0,1} or -100 (ignore)
        """

        device = active_logits.device
        dtype = active_logits.dtype

        # ====== Basic preparation ======
        mask = (active_labels != -100)            # (B, T)
        assert mask.any(), "No valid active labels found for computing active loss."

        logits_bt = active_logits.squeeze(-1)     # (B, T)
        labels_bt = active_labels.to(dtype=torch.float)  # (B, T)

        # ====== 1) Pointwise BCE with boundary weights (base term) ======
        # Default weight is 1
        weights_2d = torch.ones_like(labels_bt, dtype=dtype, device=device)

        # Compute label differences along time and upweight 0->1 / 1->0 transitions
        # Note: compare only within the same sequence to avoid cross-batch mixing
        labels_shift = torch.roll(labels_bt, shifts=1, dims=1)   # (B, T)
        mask_shift   = torch.roll(mask,      shifts=1, dims=1)   # (B, T)

        # Boundary: previous and current labels differ, and both are valid
        boundary = (labels_bt != labels_shift) & mask & mask_shift
        boundary[:, 0] = False   # First column has no previous step, so it is not a boundary

        # Increase weight at boundary points (e.g. 3x)
        weights_2d[boundary] = self.args.boundary_rate

        # Compute BCE only on masked positions
        logits_flat = logits_bt[mask]                      # (N,)
        labels_flat = labels_bt[mask]                      # (N,)
        weights_flat = weights_2d[mask]                    # (N,)

        pos_weight = torch.tensor(1.0, device=device, dtype=dtype)

        # ramp = [0.05, 0.20]
        ramp = self.args.boundary_smooth
        def soften_only_rise_1d(y, fill_vals):
            """
            y: [T] 0/1
            fill_vals: list, values corresponding to shift=1..W (larger when closer to the starting point)
                    e.g. [0.55, 0.28, 0.12, 0.05, 0.01]
            """
            y = y.float()
            T = y.numel()
            y_soft = y.clone()

            # 0->1 starting points
            starts = torch.zeros_like(y, dtype=torch.bool)
            starts[1:] = (y[1:] == 1) & (y[:-1] == 0)
            starts[0] = (y[0] == 1)

            cand = torch.zeros_like(y_soft)
            for shift, v in enumerate(fill_vals, start=1):
                tmp = torch.zeros_like(y_soft)
                tmp[:-shift] = starts[shift:].float() * float(v)
                cand = torch.maximum(cand, tmp)

            # Only raise positions that were originally 0; keep original 1s unchanged
            y_soft = torch.where(y == 0, torch.maximum(y_soft, cand), y_soft)
            y_soft[y == 1] = 1.0
            return y_soft
        labels_flat = soften_only_rise_1d(labels_flat, ramp)
        bce_loss = F.binary_cross_entropy_with_logits(
            logits_flat,
            labels_flat,
            pos_weight=pos_weight,
            weight=weights_flat,
            reduction='none'
        )

        # Normalize by the sum of weights instead of a simple average
        loss_point = (bce_loss.sum() / weights_flat.sum())

        # ====== 2) Temporal structure: intra-segment smoothing ======
        # Probability p_t
        p_bt = torch.sigmoid(logits_bt)  # (B, T)

        # Previous-step p and y
        p_shift = torch.roll(p_bt, shifts=1, dims=1)       # (B, T)
        y_shift = torch.roll(labels_bt, shifts=1, dims=1)  # (B, T)

        # Valid pair: both current and previous steps are inside the mask
        pair_mask = mask & torch.roll(mask, shifts=1, dims=1)
        pair_mask[:, 0] = False  # First column has no previous step

        # "Within the same segment" means current and previous labels are equal
        same_seg = pair_mask & (labels_bt == y_shift)

        if same_seg.any():
            diff_sq = (p_bt - p_shift) ** 2
            loss_smooth = diff_sq[same_seg].mean()
        else:
            loss_smooth = torch.zeros((), device=device, dtype=dtype)

        # ====== 3) Global speaking-rate constraint (simple version) ======
        # Keep the overall predicted speaking rate close to the true speaking rate
        p_valid = p_bt[mask]              # Model-predicted speaking probability
        y_valid = labels_bt[mask]         # Ground-truth 0/1 labels

        pred_rate = p_valid.mean()
        true_rate = y_valid.mean()

        # No need to let true_rate participate in backpropagation
        loss_rate = (pred_rate - true_rate.detach()) ** 2

        # ====== 4) Combine active loss ======
        # These hyperparameters can be tuned later; use conservative small weights for now
        # lambda_smooth = 1.0
        # lambda_rate   = 1.0
        lambda_smooth = self.args.lambda_smooth
        lambda_rate   = self.args.lambda_rate
        lambda_point = self.args.lambda_point
        active_loss = (
            lambda_point * loss_point
            + lambda_smooth * loss_smooth
            + lambda_rate   * loss_rate
        )
        # self.log({
        #     "active_loss_point": (lambda_point * loss_point).item(),
        #     "active_loss_smooth": (lambda_smooth * loss_smooth).item(),
        #     "active_loss_rate":   (lambda_rate   * loss_rate).item(),
        #     "active_loss": active_loss.item(),
        # })
        return active_loss, loss_point, loss_smooth, loss_rate


    def compute_loss_strategy1(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        outputs = model(**inputs)
        loss = outputs['loss']
        return (loss, outputs) if return_outputs else loss

    def compute_loss_strategy2(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs['labels']
        inputs['labels'] = None
        outputs = model(**inputs)
        inputs['labels'] = labels

        active_logits = outputs.active_logits
        active_labels = inputs.get("active_labels")                               
        active_loss, active_loss_point, active_loss_smooth, active_loss_rate = self.compute_active_loss(
            active_logits,
            active_labels,
        )

        outputs['main_loss'] = torch.zeros((), device=active_logits.device, dtype=active_logits.dtype)
        outputs['active_loss'] = active_loss * self.args.loss_active_scale
        loss = active_loss
        outputs['loss'] = active_loss
        return (loss, outputs) if return_outputs else loss

    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        finetune_strategy = self.args.finetune_strategy
        if finetune_strategy == 'strategy3':
            return self.compute_loss_strategy3(model, inputs, return_outputs, num_items_in_batch)
        elif finetune_strategy == "strategy2":
            return self.compute_loss_strategy2(model, inputs, return_outputs, num_items_in_batch)
        elif finetune_strategy == "strategy1":
            return self.compute_loss_strategy1(model, inputs, return_outputs, num_items_in_batch)
        else:
            raise ValueError(f"Unknown finetune stage: {finetune_strategy}")

    def compute_loss_strategy3(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        outputs = model(**inputs)
        # calculate active loss and add to main loss

        active_logits = outputs.active_logits
        active_labels = inputs.get("active_labels")     
        active_logits = active_logits[active_labels != -100].unsqueeze(0)
        active_labels = active_labels[active_labels != -100].unsqueeze(0)    
        active_loss, active_loss_point, active_loss_smooth, active_loss_rate = self.compute_active_loss(
            active_logits,
            active_labels,
        )
        # If the whole segment is silence, do not compute main-task loss
        # if torch.sum((active_labels == 1)) == 0:
        #     outputs['main_loss'] = torch.zeros((), device=active_logits.device, dtype=active_logits.dtype)
        # else:
        #     outputs['main_loss'] = outputs['loss']
        outputs['main_loss'] = outputs['loss']
        outputs['active_loss'] = active_loss * self.args.loss_active_scale
        loss = outputs['main_loss'] + outputs['active_loss']
        outputs['loss'] = loss
        self.log({
            "loss": loss.item(),
            "main_loss": outputs['main_loss'].item(),
            "active_loss": outputs['active_loss'].item(),
            "active_loss_point": active_loss_point.item(),
            "active_loss_smooth": active_loss_smooth.item(),
            "active_loss_rate": active_loss_rate.item(),
        })
        return (loss, outputs) if return_outputs else loss

    def prediction_step(self, model, inputs, prediction_loss_only, ignore_keys=None):
        model.eval()
        with torch.no_grad():
            # outputs = model(**inputs)
            loss, outputs = self.compute_loss(model, inputs, return_outputs=True)
        loss = outputs.loss                           # Original combined loss

        if prediction_loss_only:
            return (loss, None, None)
        # Prediction returns a pair: keep original prediction and also expose active prediction
        if self.args.finetune_strategy == 'strategy1':
            main_logits = outputs.logits
            main_labels = inputs.get("labels")
            return (loss, main_logits, main_labels)
        elif self.args.finetune_strategy == "strategy2":
            active_logits = outputs.active_logits
            active_labels = inputs.get("active_labels")
            return (loss, active_logits, active_labels)
        elif self.args.finetune_strategy == "strategy3":
            main_logits = outputs.logits
            main_labels = inputs.get("labels")
            active_logits = outputs.active_logits
            active_labels = inputs.get("active_labels")
            return (loss, (main_logits, active_logits), (main_labels, active_labels))
        else:
            raise ValueError(f"Unknown finetune stage: {self.args.finetune_strategy}")

    def save_model(self, output_dir: str | None = None, _internal_call: bool = False):

        output_dir = output_dir or self.args.output_dir
        os.makedirs(output_dir, exist_ok=True)
        if hasattr(self.model, "save_pretrained"):
            # Call the model's custom save method (save LoRA + state_proj)
            self.model.save_pretrained(output_dir)
        else:
            # Fall back to parent-class behavior (save state_dict)
            super().save_model(output_dir, _internal_call)