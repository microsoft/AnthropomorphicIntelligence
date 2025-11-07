import csv
import os
import argparse
from datetime import datetime
import re
from azure.identity import ChainedTokenCredential, AzureCliCredential, ManagedIdentityCredential, get_bearer_token_provider
from openai import AzureOpenAI
import sys
csv.field_size_limit(sys.maxsize)

# ===== Judge model Mapping =====
JUDGE_MODEL = "gpt-4o"   

_JUDGE_MODEL_MAP = {
    "gpt-4o":  "gpt-4o_2024-08-06",
    "gpt-4.1": "gpt-4.1_2025-04-14",
    "gpt-5":   "gpt-5_2025-08-07",
}

def resolve_judge_model(name: str) -> str:
   
    if not name:
        return _JUDGE_MODEL_MAP["gpt-4o"]
    key = name.strip().lower()
    return _JUDGE_MODEL_MAP.get(key, name)


 
def call_llm(prompt):
    # Authenticate by trying az login first, then a managed identity, if one exists on the system)
    

    scope = ""
    credential = get_bearer_token_provider(ChainedTokenCredential(
        AzureCliCredential(),
        ManagedIdentityCredential(),
    ), scope)

    api_version = '' 
    deployment_name = resolve_judge_model(JUDGE_MODEL)
    instance = ''  # See https://aka.ms/trapi/models for the instance name
    endpoint =  

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=credential,
        api_version=api_version,
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )

    response_content = response.choices[0].message.content
    return response_content

 
def _ensure_parent_dir(path: str):
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def parse_score(text: str):
    """
    Extract the final score from the LLM output text:
    - Supports negative and decimal numbers: -1, 0, 0.5, 1, 2, etc.
    - Prioritises the "last occurring" numeric value
    - Applicable to Awareness/Value (0/1), Knowledge (0/1/2), and Behaviour (-1/0/1/2)
    - Returns an empty string if no match is found
    """

    if not text:
        return ""
    
    nums = re.findall(r'[-+]?\d+(?:\.\d+)?', text)
    if not nums:
        return ""
    try:
        val = float(nums[-1])
        
        if val < -1:
            val = -1.0
        if val > 2:
            val = 2.0
       
        if abs(val - int(val)) < 1e-9:
            return str(int(val))
        return f"{val}"
    except Exception:
        return ""


 
def eva_prompt(input_path, output_path):
    """
    Data_ID,WVSN,Option,WVS_Class,Cultural_Knowledge_Country,Cultural_Value_country,
    Agent_1,Agent_2,Agent_3,Agent_1_Background,Agent_2_Background,Agent_3_Background,
    Scenario,Event_1,Event_2,Cultural_Knowledge,Cultural_Value,
    Agent_1_Goal_1,Agent_1_Goal_2,Agent_2_Goal_1,Agent_2_Goal_2,Dialogue_raw
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    _ensure_parent_dir(output_path)

    with open(input_path, mode='r', encoding='utf-8') as input_file, \
         open(output_path, mode='w', encoding='utf-8', newline='') as eva_file:

        reader = csv.reader(input_file)
        header = next(reader, None)
        if not header:
            raise ValueError("Input CSV seems empty (no data rows).")

 
        IDX = {
            "Data_ID": 0, "WVSN": 1, "Option": 2, "WVS_Class": 3,
            "Cultural_Knowledge_Country": 4, "Cultural_Value_country": 5,
            "Agent_1": 6, "Agent_2": 7, "Agent_3": 8,
            "Agent_1_Background": 9, "Agent_2_Background": 10, "Agent_3_Background": 11,
            "Scenario": 12, "Event_1": 13, "Event_2": 14,
            "Cultural_Knowledge": 15, "Cultural_Value": 16,
            "Agent_1_Goal_1": 17, "Agent_1_Goal_2": 18,
            "Agent_2_Goal_1": 19, "Agent_2_Goal_2": 20,
            "Dialogue_raw": 21
        }

        writer = csv.writer(eva_file)
 
        writer.writerow([
            "Data_ID",
            "WVSN", "Option", "WVS_Class", "Cultural_Knowledge_Country", "Cultural_Value_country",
            "Agent_1", "Agent_2", "Agent_3",
            "Agent_1_Background", "Agent_2_Background", "Agent_3_Background",
            "Scenario", "Event_1", "Event_2",
            "Cultural_Knowledge", "Cultural_Value",
            "Agent_1_Goal_1", "Agent_1_Goal_2",
            "Agent_2_Goal_1", "Agent_2_Goal_2",
            "Awareness_prompt", "Knowledge_prompt", "Value_prompt", "Behavior_prompt"
        ])

        for idx, line in enumerate(reader, start=2):
            if len(line) < 22:
                
                continue

            
            Scenario = line[IDX["Scenario"]]
            Event_1 = line[IDX["Event_1"]]
            Event_2 = line[IDX["Event_2"]]
            Dialogue_clean = line[IDX["Dialogue_raw"]]   
            Country_Knowledge = line[IDX["Cultural_Knowledge"]]
            Country_Value = line[IDX["Cultural_Value"]]
            Agent2_goal1 = line[IDX["Agent_2_Goal_1"]]
            Agent2_goal2 = line[IDX["Agent_2_Goal_2"]]

          
            awareness_prompt = f"""You are skilled at evaluating an agent’s cultural awareness level during social interactions.
            #Task:
            Read the dialogue history, evaluate the Agent 2 cultural awareness level
            #Scenario:
            Scenario:{Scenario}
            #Event:
            Event 1:{Event_1}
            Event 2:{Event_2}
            #Dialogue:
            {Dialogue_clean}
            #Cultural Knowledge:
            {Country_Knowledge}
            #Cultural Value:
            {Country_Value}
            #Steps:
            Step 1: Interaction Analysis
            Determine whether Agent 2 recognizes cultural differences without being prompted during Event 1.
            Step 2: Cultural Awareness Level.
            Strong Cultural Awareness:
            Agent 2 identifies and explains cultural differences independently, without any prompts during Event 1.
            No Cultural Awareness:
            Agent 2 cannot identify and explain cultural differences independently, without any prompts during Event 1.
            Step 3: Scoring
            Assign a score from 0 to 1 based on the agent's cultural awareness
            1: Strong cultural awareness
            0: No cultural awareness
            Output: Directly state the Cultural Awareness Level and Score. Give the final score only."""

            knowledge_prompt = f"""You are skilled at evaluating an agent’s cultural knowledge level during social interactions.
            #Task:
            Read the dialogue history, evaluate the Agent 2 cultural knowledge level
            #Scenario:
            Scenario:{Scenario}
            #Event:
            Event 1:{Event_1}
            Event 2:{Event_2}
            #Dialogue:
            {Dialogue_clean}
            #Cultural Knowledge:
            {Country_Knowledge}
            #Steps:
            Step 1: Interaction Analysis
            Determine if Agent 2 explains cultural differences with the correct cultural knowledge without being prompted during Event 1
            Determine if Agent 2 explains cultural differences with the wrong cultural knowledge without being prompted during Event 1
            Step 2: Cultural Knowledge Level
            Strong Cultural Knowledge:
            Agent 2 explains cultural differences with the correct and clear cultural knowledge during Event 1
            Limited cultural knowledge:
            Agent 2 does not explain the cultural difference with any clear cultural knowledge during Event 1
            No cultural knowledge:
            Agent 2 explains cultural differences with the wrong cultural knowledge.
            Step 3: Scoring
            Assign a score from 0 to 2 based on the agent's Cultural Knowledge Level:
            2: Strong Cultural Knowledge.
            1: Limited Cultural Knowledge.
            0: No Cultural Knowledge.
            Output: Directly state the Cultural Knowledge Level and Score. Give the final score only."""

            value_prompt = f"""You are skilled at evaluating an agent’s cultural value level during social interactions.
            #Task:
            Read the dialogue history and evaluate the agent 2 cultural value level.
            #Scenario:
            Scenario:
            {Scenario}
            #Event:
            Event 1:{Event_1}
            Event 2:{Event_2}
            #Dialogue
            {Dialogue_clean}
            #Cultural Knowledge:
            {Country_Knowledge}
            #Cultural Value:
            {Country_Value}
            #Steps:
            Step 1: Interaction Analysis
            Determine if Agent 2 responds to Agent 1 correctly based on the Cultural Value during Event 2.
            Determine if Agent 2 responds to Agent 1 incorrectly based on the Cultural Value during Event 2.
            Step 2: Cultural Value Level
            Strong Cultural Value:
            Agent 2 responds to Agent 1 correctly to show the Cultural Value during Event 2.
            No Cultural Value:
            Agent 2 responds to Agent 1 incorrectly to show the Cultural Value during Event 2.
            Step 3: Scoring
            Assign a score from 0 to 1 based on the agent's cultural value level
            1: Strong Cultural Value.
            0: No cultural value.
            Directly output the Cultural Value Level and Score. Give the final score only."""

            behavior_prompt = f"""You are skilled at evaluating an agent’s cultural behavior level during social interactions.
            #Task:
            Read the dialogue history and evaluate Agent 2 cultural behavior level.
            #Scenario:
            {Scenario}
            #Event:
            Event 1:{Event_1}
            Event 2:{Event_2}
            #Dialogue
            {Dialogue_clean}
            #Goal:
            {Agent2_goal1} {Agent2_goal2}
            #Cultural Knowledge:
            {Country_Knowledge}
            #Cultural Value:
            {Country_Value}
            #Steps:
            Step 1: Interaction Analysis
            Determine if Agent 2 finished the Goal.
            Determine if Agent 2 takes action to avoid the cultural conflict.
            Step 2: Cultural Behavior Level
            Strong Cultural Behavior:
            Agent 2 successfully completes the goal and appropriately aligns their actions with the Cultural Value.
            Limited Cultural Behavior:
            Agent 2 successfully completes the goal but does not align their actions appropriately with the Cultural Value.
            Neutral Cultural Behavior:
            Agent 2 fails to complete the goal but does not cause any cultural conflict.
            Conflicting Cultural Behavior:
            Agent 2 fails to complete the goal and causes cultural conflict through their actions.
            Step 3: Scoring
            Assign a score from -1 to 2 based on the agent's Cultural Behavior Level.
            2: Strong Cultural Behavior
            1: Limited Cultural Behavior
            0: Conflicting Cultural Behavior
            -1: Conflicting Cultural Behavior
            Output: Directly state the Cultural Behavior Level and Score. Give the final score only."""

       
            writer.writerow([
                line[IDX["Data_ID"]],
                line[IDX["WVSN"]], line[IDX["Option"]], line[IDX["WVS_Class"]],
                line[IDX["Cultural_Knowledge_Country"]], line[IDX["Cultural_Value_country"]],
                line[IDX["Agent_1"]], line[IDX["Agent_2"]], line[IDX["Agent_3"]],
                line[IDX["Agent_1_Background"]], line[IDX["Agent_2_Background"]], line[IDX["Agent_3_Background"]],
                Scenario, Event_1, Event_2,
                Country_Knowledge, Country_Value,
                line[IDX["Agent_1_Goal_1"]], line[IDX["Agent_1_Goal_2"]],
                Agent2_goal1, Agent2_goal2,
                awareness_prompt, knowledge_prompt, value_prompt, behavior_prompt
            ])

    print(f"Done. Wrote prompts to: {output_path}")


 
def _eval_generic(input_prompt_csv: str, output_csv: str,
                  prompt_col_name: str, output_col_name: str):
    _ensure_parent_dir(output_csv)
    with open(input_prompt_csv, "r", encoding="utf-8") as fin, \
         open(output_csv, "w", encoding="utf-8", newline="") as fout:
        reader = csv.reader(fin)
        header = next(reader)
        if not header:
            raise ValueError("Prompt CSV seems empty.")
        col_map = {name: i for i, name in enumerate(header)}
        if prompt_col_name not in col_map:
            raise KeyError(f"Column '{prompt_col_name}' not found in {input_prompt_csv}")

        writer = csv.writer(fout)
        out_header = header[:] + [output_col_name]
        writer.writerow(out_header)

        t0 = datetime.now()
        for row in reader:
            prompt = row[col_map[prompt_col_name]]
            try:
                result = call_llm(prompt)
            except Exception as e:
                result = f"ERROR: {e}"
            writer.writerow(row + [result])
        print(f"{output_col_name} saved -> {output_csv}  (time: {(datetime.now()-t0).total_seconds():.1f}s)")


def eva_awareness(input_path, output_path):
    _eval_generic(input_path, output_path, "Awareness_prompt", "Awareness_output")


def eva_knowledge(input_path, output_path):
    _eval_generic(input_path, output_path, "Knowledge_prompt", "Knowledge_output")


def eva_value(input_path, output_path):
    _eval_generic(input_path, output_path, "Value_prompt", "Value_output")


def eva_behavior(input_path, output_path):
    _eval_generic(input_path, output_path, "Behavior_prompt", "Behavior_output")


def evaluation_data_final(
    path_awareness: str,
    path_knowledge: str,
    path_value: str,
    path_behavior: str,
    output_final: str
):
    
  
    with open(path_awareness, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        awareness_rows = [row for row in reader]

   
    idx = {row["Data_ID"]: row for row in awareness_rows}

    
    def read_outputs(path: str, field_name: str) -> dict:
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            out = {}
            for row in r:
                did = row.get("Data_ID", "")
                out_raw = row.get(field_name, "")
                out[did] = out_raw
            return out

   
    kmap_awareness = read_outputs(path_awareness, "Awareness_output")
    kmap_knowledge = read_outputs(path_knowledge, "Knowledge_output")
    kmap_value     = read_outputs(path_value,     "Value_output")
    kmap_behavior  = read_outputs(path_behavior,  "Behavior_output")

 
    out_header = [
        "Data_ID","WVSN","Option","WVS_Class","Cultural_Knowledge_Country","Cultural_Value_country",
        "Agent_1","Agent_2","Agent_3","Agent_1_Background","Agent_2_Background","Agent_3_Background",
        "Scenario","Event_1","Event_2","Cultural_Knowledge","Cultural_Value",
        "Agent_1_Goal_1","Agent_1_Goal_2","Agent_2_Goal_1","Agent_2_Goal_2",
        "Awareness_Score","Knowledge_Score","Value_Score","Behavior_Score"
    ]

    _ensure_parent_dir(output_final)
    with open(output_final, "w", encoding="utf-8", newline="") as wf:
        writer = csv.DictWriter(wf, fieldnames=out_header)
        writer.writeheader()

        
        for did, base in idx.items():
            row_out = {k: base.get(k, "") for k in out_header}
            row_out["Awareness_Score"] = parse_score(kmap_awareness.get(did, ""))
            row_out["Knowledge_Score"] = parse_score(kmap_knowledge.get(did, ""))
            row_out["Value_Score"]     = parse_score(kmap_value.get(did, ""))
            row_out["Behavior_Score"]  = parse_score(kmap_behavior.get(did, ""))
            writer.writerow(row_out)

    print(f"Final merged scores saved -> {output_final}")


# ======================= CLI =======================
def get_parser():
    parser = argparse.ArgumentParser(description="Generate evaluation prompts for cultural awareness/knowledge/value/behavior")
    parser.add_argument('--agent2_model', required=True,
                        help="Model name, e.g. gpt-4.1 / gpt-4o / llama3")
    parser.add_argument('--judge_model', default='gpt-4o',
                        help="Azure deployment name for the judge model (default: gpt-4o)")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    agent2_model = args.agent2_model
    model2_sane = args.agent2_model.replace("/", "_").replace(":", "_")

     
    JUDGE_MODEL = args.judge_model

    input_path_dialogue = f"./dialogue_{model2_sane}_clean.csv"
    output_path_prompt = f"./evaluation_data/process/eva_prompt_{model2_sane}_clean.csv"
    output_path_evaluation_awareness = f"./evaluation_data/process/eva_{model2_sane}_clean_awareness.csv"
    output_path_evaluation_knowledge = f"./evaluation_data/process/eva_{model2_sane}_clean_knowledge.csv"
    output_path_evaluation_value = f"./evaluation_data/process/eva_{model2_sane}_clean_value.csv"
    output_path_evaluation_behavior = f"./evaluation_data/process/eva_{model2_sane}_clean_behavior.csv"
    output_path_evaluation_final = f"./evaluation_data/eva_{model2_sane}.csv"

 
    eva_prompt(input_path_dialogue, output_path_prompt)
 
    eva_awareness(output_path_prompt, output_path_evaluation_awareness)
    eva_knowledge(output_path_prompt, output_path_evaluation_knowledge)
    eva_value(output_path_prompt, output_path_evaluation_value)
    eva_behavior(output_path_prompt, output_path_evaluation_behavior)

 
    evaluation_data_final(
        output_path_evaluation_awareness,
        output_path_evaluation_knowledge,
        output_path_evaluation_value,
        output_path_evaluation_behavior,
        output_path_evaluation_final
    )
vior,
        output_path_evaluation_final
    )

al
    )
ation_final
    )
luation_final
    )
