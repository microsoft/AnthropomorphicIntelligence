# -*- coding: utf-8 -*-
"""
Hybrid Dialogue Runner:
- Agent1: Azure OpenAI (AAD token via Azure CLI)
- Agent2: Local open model (Ollama / any OpenAI-compatible endpoint)

CSV:
  data/SocialCC_Agent_1.csv
  data/SocialCC_Agent_2.csv
Out:
  dialogue_<agent2_model_sanitised>.csv
"""
import os
import csv
import time
import argparse
import data.green_logger
from autogen import ConversableAgent
from azure.identity import AzureCliCredential, get_bearer_token_provider


def get_parser():
    p = argparse.ArgumentParser(description="SocialCC Dialogue Generation (Azure GPT-4o + Ollama)")
    # Agent1 (Azure)
    p.add_argument("--agent1_deployment", default="gpt-4o",
                   help="Azure OpenAI deployment name for Agent1 (default: gpt-4o).")
    p.add_argument("--azure_endpoint", default="",
                   help="Azure OpenAI endpoint, e.g. https://<resource>.openai.azure.com "
                        "(default: env AZURE_OPENAI_ENDPOINT).")
    p.add_argument("--azure_api_version", default="",
                   help="Azure OpenAI API version (default: 2025-01-01-preview).")

    # Agent2 (Local open model)
    p.add_argument("--agent2_model", required=True,default="llama2:7b-chat",
                   help="Local open model name for Agent2, e.g. llama2:7b-chat / llama3.1:8b-instruct")
    p.add_argument("--base_url", default="http://localhost:11434/v1",
                   help="OpenAI-compatible base URL for Agent2 (default: Ollama http://localhost:11434/v1)")
    p.add_argument("--temperature", type=float, default=1.0,
                   help="Sampling temperature for both agents (default: 1.0)")

    # Misc
    # p.add_argument("--max_rows", type=int, default=3,
    #                help="Process at most N rows from each CSV (default: 3; set -1 for all)")
    return p


def _azure_llm_config(deployment: str, endpoint: str, api_version: str, temperature: float):
    """
    Build Autogen config for Azure OpenAI using AAD token (Azure CLI).
    """
    if not endpoint:
        raise ValueError("Azure endpoint is required. Set --azure_endpoint or env AZURE_OPENAI_ENDPOINT.")
    # AAD token provider via CLI login
    credential = AzureCliCredential()
    token_provider = get_bearer_token_provider(
        credential, ""
    )
 
    return {
        "config_list": [
            {
                "model": deployment,                 
                "api_type": "azure",
                "base_url": endpoint,                
                "api_version": api_version,
                "azure_ad_token_provider": token_provider,
                "temperature": temperature,
                "price": [0.0, 0.0],  
            }
        ],
        "cache_seed": None,
    }


def _local_llm_config(model_name: str, base_url: str, temperature: float):
 
    if not base_url.endswith("/v1"):
        base_url = base_url.rstrip("/") + "/v1"
    return {
        "config_list": [
            {
                "model": model_name,
                "base_url": base_url,          
                "api_key": "ollama",           
                "temperature": temperature,
                "extra_body": {"options": {"num_ctx": 4096}},
            }
        ],
        "cache_seed": None,
    }



def build_clients_and_configs(agent1_deployment: str, azure_endpoint: str, azure_api_version: str,
                              agent2_model: str, base_url: str, temperature: float):
    cfg1 = _azure_llm_config(agent1_deployment, azure_endpoint, azure_api_version, temperature)
    cfg2 = _local_llm_config(agent2_model, base_url, temperature)
    return cfg1, cfg2


# def run_dialogue(agent1_path: str, agent2_path: str, output_path: str,
#                  cfg1, cfg2, max_rows: int):

def run_dialogue(agent1_path: str, agent2_path: str, output_path: str,
                 cfg1, cfg2):
    start = time.time()

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(agent1_path, mode='r', newline='', encoding='utf-8') as f1, \
         open(agent2_path, mode='r', newline='', encoding='utf-8') as f2, \
         open(output_path, mode='w', newline='', encoding='utf-8') as fout:

        r1, r2 = csv.reader(f1), csv.reader(f2)
        next(r1, None)
        next(r2, None)
        d1 = [row for row in r1]
        d2 = [row for row in r2]
        # if max_rows is not None and max_rows > 0:
        #     d1, d2 = d1[:max_rows], d2[:max_rows]

        w = csv.writer(fout)
        w.writerow([
            "Data_ID", "WVSN", "Option", "WVS_Class", "Country_Knowledge_Country", "Country_Value_Country",
            "Agent_1", "Agent_2", "Agent_3", "Agent_1_Background", "Agent_2_Background", "Agent_3_Background",
            "Scenario", "Event_1", "Event_2", "Country_Knowledge", "Country_Value",
            "Agent1_goal1", "Agent1_goal2", "Agent2_goal1", "Agent2_goal2", "row"
        ])

        for a1, a2 in zip(d1, d2):
            
            if len(a1) <= 21 or len(a2) <= 21:
                raise ValueError(f"CSV row too short. Got len(a1)={len(a1)}, len(a2)={len(a2)}")

            
            Data_ID, WVSN, Option, WVS_Class = a1[0], a1[1], a1[2], a1[3]
            Country_Knowledge_Country, Country_Value_Country = a1[4], a1[5]
            Agent_1, Agent_2, Agent_3 = a1[6], a1[7], a1[8]
            Agent_1_Background, Agent_2_Background, Agent_3_Background = a1[9], a1[10], a1[11]
            Scenario, Event_1, Event_2 = a1[12], a1[13], a1[14]
            Country_Knowledge, Country_Value = a1[15], a1[16]
            Agent1_goal1, Agent1_goal2, Agent2_goal1, Agent2_goal2 = a1[17], a1[18], a1[19], a1[20]

            SYSTEM_MESSAGE_CFP_WRITER = a1[21]
            SYSTEM_MESSAGE_CFP_REVIEWER = a2[21]

            
            writer = ConversableAgent(
                name="SocialDuolingoAgent1",
                system_message=SYSTEM_MESSAGE_CFP_WRITER,
                llm_config=cgf_safe(cfg1),
                code_execution_config=False,
                human_input_mode="NEVER",
                function_map=None,
                is_termination_msg=_default_termination_check,
                silent=True,
            )
            reviewer = ConversableAgent(
                name="SocialDuolingoAgent2",
                system_message=SYSTEM_MESSAGE_CFP_REVIEWER,
                llm_config=cgf_safe(cfg2),
                code_execution_config=False,
                human_input_mode="NEVER",
                function_map=None,
                is_termination_msg=_default_termination_check,
                silent=True,
            )

           
            initial = writer.generate_reply(messages=[{"content": "", "role": "user"}])
            result = writer.initiate_chat(
                reviewer,
                clear_history=False,
                message=initial
            )
            chat_history = result.chat_history
            row_dump = [m for m in chat_history]

            w.writerow([
                Data_ID, WVSN, Option, WVS_Class, Country_Knowledge_Country, Country_Value_Country,
                Agent_1, Agent_2, Agent_3, Agent_1_Background, Agent_2_Background, Agent_3_Background,
                Scenario, Event_1, Event_2, Country_Knowledge, Country_Value,
                Agent1_goal1, Agent1_goal2, Agent2_goal1, Agent2_goal2, row_dump
            ])

    print("finished")
    print(f"Run Time: {time.time() - start:.2f}s")
    print(f"Output → {output_path}")


def cgf_safe(cfg):
    
    return cfg if isinstance(cfg, dict) else {"config_list": cfg}


def _default_termination_check(msg):
    return isinstance(msg, dict) and isinstance(msg.get("content"), str) and ("good bye" in msg["content"].lower())


def main():
    args = get_parser().parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    agent1_csv = os.path.join(data_dir, "SocialCC_Agent_1.csv")
    agent2_csv = os.path.join(data_dir, "SocialCC_Agent_2.csv")

    model2_sane = args.agent2_model.replace("/", "_").replace(":", "_")
    out_path = os.path.join(base_dir, f"dialogue_{model2_sane}.csv")

    cfg1, cfg2 = build_clients_and_configs(
        agent1_deployment=args.agent1_deployment,
        azure_endpoint=args.azure_endpoint,
        azure_api_version=args.azure_api_version,
        agent2_model=args.agent2_model,
        base_url=args.base_url,
        temperature=args.temperature
    )
    # run_dialogue(agent1_csv, agent2_csv, out_path, cfg1, cfg2, args.max_rows)
    run_dialogue(agent1_csv, agent2_csv, out_path, cfg1, cfg2)


if __name__ == "__main__":
    main()
g2)


if __name__ == "__main__":
    main()
in__":
    main()
__name__ == "__main__":
    main()
