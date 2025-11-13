#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import ast
import argparse
from pathlib import Path
import sys
csv.field_size_limit(sys.maxsize)
HEADER = [
    "Data_ID","WVSN","Option","WVS_Class","Cultural_Knowledge_Country","Cultural_Value_country",
    "Agent_1","Agent_2","Agent_3","Agent_1_Background","Agent_2_Background","Agent_3_Background",
    "Scenario","Event_1","Event_2","Cultural_Knowledge","Cultural_Value",
    "Agent_1_Goal_1","Agent_1_Goal_2","Agent_2_Goal_1","Agent_2_Goal_2","Dialogue_raw"
]

def clean_chat_history(read_file_path: Path, write_file_path: Path) -> None:
    with read_file_path.open(mode='r', encoding='utf-8', newline='') as input_file, \
         write_file_path.open(mode='w', encoding='utf-8', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        # skip header row from source
        next(reader, None)
        writer.writerow(HEADER)

        for line in reader:
            # Expecting at least 22 columns (index 0..21)
            if len(line) < 22:
                # Skip malformed rows gracefully
                continue

            Data_ID = line[0]
            WVSN = line[1]
            Option = line[2]
            WVS_Class = line[3]
            Country_Knowledge_Country = line[4]
            Country_Value_Country = line[5]
            Agent_1 = line[6]
            Agent_2 = line[7]
            Agent_3 = line[8]
            Agent_1_Background = line[9]
            Agent_2_Background = line[10]
            Agent_3_Background = line[11]
            Scenario = line[12]
            Event_1 = line[13]
            Event_2 = line[14]
            Country_Knowledge = line[15]
            Country_Value = line[16]
            Agent1_goal1 = line[17]
            Agent1_goal2 = line[18]
            Agent2_goal1 = line[19]
            Agent2_goal2 = line[20]

            # Column 21 is the raw chat history string
            chat_history_str = line[21].strip().strip('"')

            output_text = ""
            if chat_history_str:
                try:
                    chat_history_list = ast.literal_eval(chat_history_str)
                except Exception:
                    # If parsing fails, just dump the raw text
                    chat_history_list = []

                if isinstance(chat_history_list, list):
                    round_num = 1
                    for i in range(0, len(chat_history_list), 2):
                        if i + 1 < len(chat_history_list):
                            agent_1_turn = chat_history_list[i]
                            agent_2_turn = chat_history_list[i + 1]
                            a1_content = agent_1_turn.get('content', '')
                            a2_content = agent_2_turn.get('content', '')
                            output_text += (
                                f"Round {round_num}:\n"
                                f"Agent 1:\n{a1_content}\n"
                                f"Agent 2:\n{a2_content}\n"
                            )
                        else:
                            agent_1_turn = chat_history_list[i]
                            a1_content = agent_1_turn.get('content', '')
                            output_text += (
                                f"Round {round_num}:\n"
                                f"Agent 1:\n{a1_content}\n"
                            )
                        round_num += 1
                else:
                    # Fallback if not list
                    output_text = str(chat_history_str)

            row_out = [
                Data_ID, WVSN, Option, WVS_Class, Country_Knowledge_Country, Country_Value_Country,
                Agent_1, Agent_2, Agent_3, Agent_1_Background, Agent_2_Background, Agent_3_Background,
                Scenario, Event_1, Event_2, Country_Knowledge, Country_Value,
                Agent1_goal1, Agent1_goal2, Agent2_goal1, Agent2_goal2, output_text
            ]
            writer.writerow(row_out)


def get_parser():
    parser = argparse.ArgumentParser(description="Clean dialogue CSV by formatting chat history into rounds.")
    parser.add_argument('--agent2_model', required=True,
                        help="Model name to select input/output files, e.g., gpt-4.1")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    # File name pattern in current directory
    # Input: dialogue-<model>.csv -> Output: dialogue-<model>_clean.csv
    # e.g., gpt-4.1 => dialogue-gpt-4.1.csv / dialogue-gpt-4.1_clean.csv
    # model_tag = args.agent2_model
    model2_sane = args.agent2_model.replace("/", "_").replace(":", "_")
    read_file = Path.cwd() / f"dialogue_{model2_sane}.csv"
    write_file = Path.cwd() / f"dialogue_{model2_sane}_clean.csv"

    if not read_file.exists():
        sys.stderr.write(f"[Error] Input file not found: {read_file}\n")
        sys.exit(1)

    clean_chat_history(read_file, write_file)
    print(f"[Done] Wrote cleaned file to: {write_file}")


if __name__ == "__main__":
    main()
