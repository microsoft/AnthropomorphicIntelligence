import csv
import argparse
import os
from typing import Tuple, Dict

SCORE_COLS = [
    "Awareness_Score",
    "Knowledge_Score",
    "Value_Score",
    "Behavior_Score",
]

OUT_HEADER = [
    "Model",
    "Awareness Performance",
    "Knowledge Performance",
    "Value Performance",
    "Behavior Performance",
]


def get_parser():
    parser = argparse.ArgumentParser(description="Compute mean scores")
    parser.add_argument('--agent2_model', required=True,
                        help="LLM name for agent2, e.g. gpt-4.1 / gpt-4o / llama3-8b")
    return parser


def safe_float(x: str):
    try:
        return float(x.strip())
    except Exception:
        return None


def compute_means(input_csv: str) -> Dict[str, float]:
    totals = {k: 0.0 for k in SCORE_COLS}
    counts = {k: 0 for k in SCORE_COLS}

    with open(input_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # sanity check header contains required columns
        missing = [c for c in SCORE_COLS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"Input file missing columns: {missing}. "
                             f"Got columns: {reader.fieldnames}")

        for row in reader:
            for col in SCORE_COLS:
                v = safe_float(row.get(col, ""))
                if v is not None:
                    totals[col] += v
                    counts[col] += 1

    means = {}
    for col in SCORE_COLS:
        if counts[col] == 0:
            means[col] = 0.0
        else:
            means[col] = totals[col] / counts[col]
    return means


def main():
    args = get_parser().parse_args()
    agent2_model = args.agent2_model
    model2_sane = args.agent2_model.replace("/", "_").replace(":", "_")

    input_path_evaluation_final = f"./evaluation_data/eva_{model2_sane}.csv"
    output_path_evaluation_final = f"./result/result_{model2_sane}.csv"

    if not os.path.exists(input_path_evaluation_final):
        raise FileNotFoundError(f"Input not found: {input_path_evaluation_final}")

    means = compute_means(input_path_evaluation_final)

    os.makedirs(os.path.dirname(output_path_evaluation_final), exist_ok=True)

    # write single-row CSV
    with open(output_path_evaluation_final, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(OUT_HEADER)
        writer.writerow([
            agent2_model,
            f"{means['Awareness_Score']:.6f}",
            f"{means['Knowledge_Score']:.6f}",
            f"{means['Value_Score']:.6f}",
            f"{means['Behavior_Score']:.6f}",
        ])

    print(f"Wrote results to: {output_path_evaluation_final}")


if __name__ == "__main__":
    main()
