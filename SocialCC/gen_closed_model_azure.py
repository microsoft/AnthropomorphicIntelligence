import os
import csv
import time
import argparse
import data.green_logger
import autogen
from autogen import ConversableAgent
from openai import AzureOpenAI
from azure.identity import get_bearer_token_provider, AzureCliCredential


def get_parser():
    parser = argparse.ArgumentParser(description="SocialCC Dialogue Generation")
    parser.add_argument('--agent2_model', required=True,
                        help="LLM name for agent2, e.g. gpt-4.1 / gpt-4o / gpt-4o-mini")
    return parser


def build_clients_and_configs(agent2_model: str):
     
    credential = AzureCliCredential()
    token_provider = get_bearer_token_provider(
        credential,
        ""
    )

    

    config_list_agent1 = [
        {
            'model': "gpt-4o",
            "api_type": "azure",
            "base_url": "",   
            "api_version": "",
            "azure_ad_token_provider": token_provider
        }
    ]

    config_list_agent2 = [
        {
            'model': agent2_model,   
            "api_type": "azure",
            "base_url": "",   
            "api_version": "",
            "azure_ad_token_provider": token_provider
        }
    ]

    return config_list_agent1, config_list_agent2


def run_dialogue(agent1_path: str, agent2_path: str, output_path: str, agent2_model: str):
    
    start_time = time.time()

   
    data_dir = os.path.dirname(agent1_path)
    os.makedirs(data_dir, exist_ok=True)

    config_list_agent1, config_list_agent2 = build_clients_and_configs(agent2_model)

    with open(agent1_path, mode='r', newline='', encoding='utf-8') as agent1_file, \
         open(agent2_path, mode='r', newline='', encoding='utf-8') as agent2_file, \
         open(output_path, mode='w', newline='', encoding='utf-8') as out_file:

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
                is_termination_msg=lambda msg: "good bye" in msg["content"].lower(),
                silent=True,
            )

            cfp_reviewer = ConversableAgent(
                name="SocialDuolingoAgent2",
                system_message=SYSTEM_MESSAGE_CFP_REVIEWER,
                llm_config={"config_list": config_list_agent2},
                code_execution_config=False,
                human_input_mode="NEVER",
                function_map=None,
                is_termination_msg=lambda msg: "good bye" in msg["content"].lower(),
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

            output_row = [
                Data_ID, WVSN, Option, WVS_Class, Country_Knowledge_Country, Country_Value_Country,
                Agent_1, Agent_2, Agent_3, Agent_1_Background, Agent_2_Background, Agent_3_Background,
                Scenario, Event_1, Event_2, Country_Knowledge, Country_Value,
                Agent1_goal1, Agent1_goal2, Agent2_goal1, Agent2_goal2, row
            ]
            writer.writerow(output_row)

    duration = time.time() - start_time
    print("finished")
    print(f"Run Time: {duration:.2f}s")
    print(f"Output → {output_path}")


def main():
    parser = get_parser()
    args = parser.parse_args()

    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    agent1_path = os.path.join(DATA_DIR, "SocialCC_Agent_1.csv")
    agent2_path = os.path.join(DATA_DIR, "SocialCC_Agent_2.csv")
    
    model_name_sanitised = args.agent2_model.replace("/", "_").replace(":", "_")

    output_path = os.path.join(BASE_DIR, f"dialogue_{model_name_sanitised}.csv")


    
    run_dialogue(
        agent1_path=agent1_path,
        agent2_path=agent2_path,
        output_path=output_path,
        agent2_model=args.agent2_model
    )


if __name__ == "__main__":
    main()
