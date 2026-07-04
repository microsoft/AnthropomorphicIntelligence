from dataclasses import dataclass, field
from typing import List, Optional

from transformers import TrainingArguments


@dataclass
class CompanionTrainingArguments(TrainingArguments):
    """
    Companion training arguments, extending the base TrainingArguments class.
    """
    # debug: bool = field(
    #     default=False,
    #     metadata={"help": "Enable debug mode."}
    # )
    # report_to: List[str] = field(
    #     default_factory=lambda: ["wandb", "swan"],
    #     metadata={"help": "List of integrations to report results and logs to."}
    # )

    debug_port: int = field(
        default=9501,
        metadata={"help": "Port for debugpy."}
    )
    use_lora: bool = field(
        default=True,
        metadata={"help": "Whether to use LoRA for training."}
    )
    lora_enable: bool = field(
        default=True,
        metadata={"help": "Whether to use LoRA for training."}
    )
    lora_r: int = field(
        default=16,
        metadata={"help": "LoRA rank."}
    )
    lora_alpha: int = field(
        default=32,
        metadata={"help": "LoRA alpha."}
    )
    lora_dropout: float = field(
        default=0.05,
        metadata={"help": "LoRA dropout."}
    )
    lora_target_modules: List[str] = field(
        # default_factory=lambda: [
        #     "embed_tokens", "q_proj", "k_proj", "v_proj",
        #     "o_proj", "gate_proj", "up_proj", "down_proj"
        # ],
        default_factory=lambda: [
            "q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj", "embed_tokens", "lm_head"
        ],
        metadata={"help": "Target modules for LoRA."}
    )
    freeze_audio: bool = field(
        default=True,
        metadata={"help": "Whether to freeze the audio tower."}
    )
    freeze_visual: bool = field(
        default=True,
        metadata={"help": "Whether to freeze the visual tower."}
    )
    lambda_smooth: float = field(
        default=1.0,
        metadata={"help": "active loss"}
    )
    lambda_rate: float = field(
        default=1.0,
        metadata={"help": "active loss"}
    )
    lambda_point: float = field(
        default=1.0,
        metadata={"help": "active loss"}
    )
    boundary_rate: float = field(
        default=5.0,
        metadata={"help": "boundary rate"}
    )
    boundary_smooth: List[float] = field(
        default_factory=lambda: [0.05, 0.20],
        metadata={"help": "boundary smooth"}
    )
    finetune_strategy: str = field(
        default="strategy1",
        metadata={"help": "Finetuning strategy: strategy1, strategy2 or strategy3."}
    )
    loss_active_scale: float = field(
        default=1.0,
        metadata={"help": "Scale the loss for active state."}
    )
    # train_audio


@dataclass
class CompanionModelArguments:
    """
    Companion model arguments.
    """
    model_name_or_path: Optional[str] = field(
        default="Qwen/Qwen2.5-Omni-7B",
        metadata={"help": "Load pretrained model from a specific path or model name."}
    )
    enable_audio_output: bool = field(
        default=False,
        metadata={"help": "Enable talker for Qwen2.5-Omni Model."}
    )
    state_threshold: float = field(
        default=0.5,
        metadata={"help": "Threshold to decide the active state."}
    )
    add_special_tokens: bool = field(
        default=False,
        metadata={"help": "Whether to add special tokens to the tokenizer."}
    )
    active_layer_id: int = field(
        default=-1,
        metadata={"help": "Which layer's hidden state to use for state classification. -1 means the last layer."}
    )
    ckpt_path: Optional[str] = field(
        default=None,
        metadata={"help": "Path to the checkpoint for resuming training."}
    )

    
@dataclass
class CompanionDataArguments:
    """
    Companion data arguments.
    """
    train_dataset_names: List[str] = field(
        default_factory=list,
        metadata={"help": "List of dataset names."}
    )
    val_dataset_names: List[str] = field(
        default_factory=list,
        metadata={"help": "List of validation dataset names."}
    )
    # train_dataset_path: Optional[str] = field(
    #     default="./dataset/train/VoiceAssistant_one-turn_data_470K_train.json",
    #     metadata={"help": "Path to the training dataset."}
    # )
    # eval_dataset_path: Optional[str] = field(
    #     default="./dataset/validation/VoiceAssistant_one-turn_data_470K_validation.json",
    #     metadata={"help": "Path to the evaluation dataset."}
    # )

    use_audio_in_video: Optional[bool] = field(
        default=False,
        metadata={"help": "Whether to use audio in video."}
    )
    video_clip_length: int = field(
        default=90,
        metadata={"help": "Video clip length."}
    )
    # data_dir_path: List[str] = field(
    #     default_factory=list,
    #     metadata={"help": "Path to the data dir."}
    # )
    data_dir_path: str = field(
        default="",
        metadata={"help": "Path to the data dir."}
    )
    min_pixels: int = field(
        default=100352,
        metadata={"help": "Minimum pixels for image resizing."}
    )
    max_pixels: int = field(
        default=100352,
        metadata={"help": "Maximum pixels for image resizing."}
    )