#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SocialCC Dialogue Generation (OpenAI Official API Key via Autogen JSON configs)

Use autogen.config_list_from_json("model_config_*.json") to load configuration files.

The API key is injected through environment variables or a .env file; the JSON supports the placeholder "$OPENAI_API_KEY".

The --agent2_model argument can override the model field of the second agent.
"""

import os
import csv
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any
import data.green_logger
import autogen
from autogen import ConversableAgent
from dotenv import load_dotenv








# ---------- Path & Environment ----------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
load_dotenv(BASE_DIR / ".env")   


def get_parser():
    parser = argparse.ArgumentParser(description="SocialCC Dialogue Generation")
    parser.add_argument(
        '--agent2_model',
        required=True,
        help="LLM name for agent2, e.g. gpt-4.1 / gpt-4o / gpt-4o-mini"
    )
    parser.add_argument(
        '--cfg_agent1',
        default=str(BASE_DIR / "model_config_agent1.json"),
        help="JSON config for Agent1 (default: model_config_agent1.json)"
    )
    parser.add_argument(
        '--cfg_agent2',
        default=str(BASE_DIR / "model_config_agent2.json"),
        help="JSON config for Agent2 (default: model_config_agent2.json)"
    )
    return parser


 
def _inject_env_api_keys(cfg_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
     
    for cfg in cfg_list:
        key = cfg.get("api_key")
        if isinstance(key, str) and key.startswith("$"):
            env_name = key[1:]
            value = os.getenv(env_name)
            if not value:
                raise ValueError(
                  
                    f'The environment variable {env_name} is not set, but "{key}" is used as a placeholder in the configuration file.'
                )
            cfg["api_key"] = value
        elif not key:
            env_value = os.getenv("OPENAI_API_KEY")
            if not env_value:
                raise ValueError(
                    "The configuration does not include an api_key, and the environment variable OPENAI_API_KEY is not set."
                )

            cfg["api_key"] = env_value
    return cfg_list


def load_config_list(json_path: str, model_override: str = None) -> List[Dict[str, Any]]:
  
    cfg_list = autogen.config_list_from_json(json_path)
    if not isinstance(cfg_list, list) or not cfg_list:
        raise ValueError(f"{json_path} did not return a valid config_list.")


     
    cfg_list = _inject_env_api_keys(cfg_list)

 
    if model_override:
        for cfg in cfg_list:
            cfg["model"] = model_override

  
    for cfg in cfg_list:
        cfg.setdefault("api_type", "openai")
        cfg.setdefault("base_url", "https://api.openai.com/v1")

    return cfg_list

 
def build_clients_and_configs(agent2_model: str, cfg_agent1_path: str, cfg_agent2_path: str):
    
    config_list_agent1 = load_config_list(cfg_agent1_path, model_override=None)
    config_list_agent2 = load_config_list(cfg_agent2_path, model_override=agent2_model)
    return config_list_agent1, config_list_agent2


def run_dialogue(agent1_path: Path, agent2_path: Path, output_path: Path,
                 config_list_agent1: List[Dict[str, Any]],
                 config_list_agent2: List[Dict[str, Any]]):
    start_time = time.time()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with agent1_path.open('r', newline='', encoding='utf-8') as agent1_file, \
         agent2_path.open('r', newline='', encoding='utf-8') as agent2_file, \
         output_path.open('w', newline='', encoding='utf-8') as out_file:

        agent1_reader = csv.reader(agent1_file)
        agent2_reader = csv.reader(agent2_file)

        
        next(agent1_reader, None)
        next(agent2_reader, None)

       
        agent1_data = [row for row in agent1_reader]
        agent2_data = [row for row in agent2_reader]

        writer = csv.writer(out_file)
        writer.writerow([
            "Data_ID", "WVSN", "Option", "WVS_Class", "Country_Knowledge_Country", "Country_Value_Country",
            "Agent_1", "Agent_2", "Agent_3", "Agent_1_Background", "Agent_2_Background", "Agent_3_Background",
            "Scenario", "Event_1", "Event_2", "Country_Knowledge", "Country_Value",
            "Agent1_goal1", "Agent1_goal2", "Agent2_goal1", "Agent2_goal2", "row"
        ])

        for agent1_line, agent2_line in zip(agent1_data, agent2_data):
             
            Data_ID = agent1_line[0]
            WVSN = agent1_line[1]
            Option = agent1_line[2]
            WVS_Class = agent1_line[3]
            Country_Knowledge_Country = agent1_line[4]
            Country_Value_Country = agent1_line[5]
            Agent_1 = agent1_line[6]
            Agent_2 = agent1_line[7]
            Agent_3 = agent1_line[8]
            Agent_1_Background = agent1_line[9]
            Agent_2_Background = agent1_line[10]
            Agent_3_Background = agent1_line[11]

            Scenario = agent1_line[12]
            Event_1 = agent1_line[13]
            Event_2 = agent1_line[14]
            Country_Knowledge = agent1_line[15]
            Country_Value = agent1_line[16]
            Agent1_goal1 = agent1_line[17]
            Agent1_goal2 = agent1_line[18]
            Agent2_goal1 = agent1_line[19]
            Agent2_goal2 = agent1_line[20]

            SYSTEM_MESSAGE_CFP_WRITER = agent1_line[21]
            SYSTEM_MESSAGE_CFP_REVIEWER = agent2_line[21]

 
            cfp_writer = ConversableAgent(
                name="SocialDuolingoAgent1",
                system_message=SYSTEM_MESSAGE_CFP_WRITER,
                llm_config={"config_list": config_list_agent1},
                code_execution_config=False,
                human_input_mode="NEVER",
                function_map=None,
                is_termination_msg=lambda msg: (
                    isinstance(msg, dict)
                    and isinstance(msg.get("content", ""), str)
                    and ("good bye" in msg["content"].lower())
                ),
                silent=True,
            )

            cfp_reviewer = ConversableAgent(
                name="SocialDuolingoAgent2",
                system_message=SYSTEM_MESSAGE_CFP_REVIEWER,
                llm_config={"config_list": config_list_agent2},
                code_execution_config=False,
                human_input_mode="NEVER",
                function_map=None,
                is_termination_msg=lambda msg: (
                    isinstance(msg, dict)
                    and isinstance(msg.get("content", ""), str)
                    and ("good bye" in msg["content"].lower())
                ),
                silent=True,
            )

 
            initial_cfp_generation_reply = cfp_writer.generate_reply(
                messages=[{"content": "", "role": "user"}]
            )

            result = cfp_writer.initiate_chat(
                cfp_reviewer,
                clear_history=False,
                message=initial_cfp_generation_reply
            )

            chat_history = result.chat_history
            row = [msg for msg in chat_history]

            writer.writerow([
                Data_ID, WVSN, Option, WVS_Class, Country_Knowledge_Country, Country_Value_Country,
                Agent_1, Agent_2, Agent_3, Agent_1_Background, Agent_2_Background, Agent_3_Background,
                Scenario, Event_1, Event_2, Country_Knowledge, Country_Value,
                Agent1_goal1, Agent1_goal2, Agent2_goal1, Agent2_goal2, row
            ])

    duration = time.time() - start_time
    print("finished")
    print(f"Run Time: {duration:.2f}s")
    print(f"Output → {output_path}")


def main():
    args = get_parser().parse_args()

    agent1_path = DATA_DIR / "SocialCC_Agent_1.csv"
    agent2_path = DATA_DIR / "SocialCC_Agent_2.csv"
 
    model_name_sanitised = args.agent2_model.replace("/", "_").replace(":", "_")
    output_path = BASE_DIR / f"dialogue_{model_name_sanitised}.csv"

    cfg1, cfg2 = build_clients_and_configs(
        agent2_model=args.agent2_model,
        cfg_agent1_path=args.cfg_agent1,
        cfg_agent2_path=args.cfg_agent2,
    )

    run_dialogue(
        agent1_path=agent1_path,
        agent2_path=agent2_path,
        output_path=output_path,
        config_list_agent1=cfg1,
        config_list_agent2=cfg2,
    )


if __name__ == "__main__":
    main()
