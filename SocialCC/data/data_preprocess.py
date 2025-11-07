import csv
import os
from typing import List

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR
INPUT_CSV = os.path.join(DATA_DIR, "SocialCC.csv")
OUT_AGENT1 = os.path.join(DATA_DIR, "SocialCC_Agent_1.csv")
OUT_AGENT2 = os.path.join(DATA_DIR, "SocialCC_Agent_2.csv")

HEADER: List[str] = [
    "Data_ID", "WVSN", "Option", "WVS_Class", "Cultural_Knowledge_Country",
    "Cultural_Value_country", "Agent_1", "Agent_2", "Agent_3",
    "Agent_1_Background", "Agent_2_Background", "Agent_3_Background",
    "Scenario", "Event_1", "Event_2", "Cultural_Knowledge", "Cultural_Value",
    "Agent_1_Goal_1", "Agent_1_Goal_2", "Agent_2_Goal_1", "Agent_2_Goal_2",
    "Prompt",
]


def _clean(val: str) -> str:
    if val is None:
        return ""
    # normalise newlines and trim
    return str(val).replace("\r", " ").strip()


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def build_agent_1_prompt(row: List[str]) -> str:
    Data_ID = _clean(row[0])
    WVSN_id = _clean(row[1])
    option = int(float(row[2])) if _clean(row[2]) else 0
    WVS_Class = _clean(row[3])
    Cultural_Knowledge_country = _clean(row[4])
    Cultural_Value_country = _clean(row[5])
    agent1 = _clean(row[6])
    agent2 = _clean(row[7])
    agent3 = _clean(row[8])
    Agent_1_Background = _clean(row[9])
    Agent_2_Background = _clean(row[10])
    Agent_3_Background = _clean(row[11])
    Relationship = _clean(row[12])
    Scenario = _clean(row[13])
    Event_1 = _clean(row[14])
    Event_2 = _clean(row[15])
    Cultural_Knowledge = _clean(row[16])
    Cultural_Value = _clean(row[17])
    Agent_1_Goal_1 = _clean(row[18])
    Agent_1_Goal_2 = _clean(row[19])

    if agent3:
        prompt = f"""
# Task
Act as {agent1} in the scenario and interact with {agent2} to achieve your goal.

# Scenario
{Scenario}

# Events
- Event 1: {Event_1}
- Event 2: {Event_2}

# Characters
- Character 1: {Agent_1_Background}
- Character 2: {Agent_2_Background}
- Character 3: {Agent_3_Background}

# Cultural Knowledge
{Cultural_Knowledge}

# Cultural Value
{Cultural_Value}

# Goals (for you)
- Goal 1: {Agent_1_Goal_1}
- Goal 2: {Agent_1_Goal_2}

# Dialogue Rules
1. Interact with {agent2} to achieve each goal one by one.
2. While working toward each goal, mention content that may cause cultural conflict to test {agent2}'s cultural intelligence.
3. If {agent2} agrees with your suggestion, follow up by asking if they realise it might be considered socially unacceptable, without directly providing clear cultural knowledge.
4. If {agent2} does not realise the suggestion is culturally unacceptable, follow up by asking if they are aware of its inappropriateness and then provide clear cultural knowledge.
5. If {agent2} disagrees without providing reasons related to cultural knowledge, follow up by asking if they realise the suggestion might be considered socially unacceptable, without directly offering clear cultural knowledge.
6. Complete the task within 20 rounds of dialogue.
7. Once all goals are achieved, end the dialogue with "OK. GOOD BYE!".
8. Your first sentence should be "Hello".
""".strip()
    else:
        prompt = f"""
# Task
Act like {agent1} in the scenario and interact with {agent2} to achieve your goal.

# Scenario
{Scenario}

# Events
- Event 1: {Event_1}
- Event 2: {Event_2}

# Characters
- Character 1: {Agent_1_Background}
- Character 2: {Agent_2_Background}

# Relationship
{Relationship}

# Cultural Knowledge
{Cultural_Knowledge}

# Cultural Value
{Cultural_Value}

# Goals (for you)
- Goal 1: {Agent_1_Goal_1}
- Goal 2: {Agent_1_Goal_2}

# Dialogue Rules
1. Interact with {agent2} to achieve each goal one by one.
2. While working toward each goal, mention content that may cause cultural conflict to test {agent2}'s cultural intelligence.
3. If {agent2} agrees with your suggestion, follow up by asking if they realise it might be considered socially unacceptable, without directly providing clear cultural knowledge.
4. If {agent2} does not realise the suggestion is culturally unacceptable, follow up by asking if they are aware of its inappropriateness and provide clear cultural knowledge.
5. If {agent2} disagrees without providing reasons related to cultural knowledge, follow up by asking if they realise the suggestion might be considered socially unacceptable, without directly offering clear cultural knowledge.
6. Complete the task within 20 rounds of dialogue.
7. Once all goals are achieved, end the dialogue with "OK. GOOD BYE!".
8. Your first sentence should be "Hello".
""".strip()

    return Data_ID, WVSN_id, option, WVS_Class, Cultural_Knowledge_country, Cultural_Value_country, agent1, agent2, agent3, \
        Agent_1_Background, Agent_2_Background, Agent_3_Background, Scenario, Event_1, Event_2, \
        Cultural_Knowledge, Cultural_Value, Agent_1_Goal_1, Agent_1_Goal_2, _clean(row[20]), _clean(row[21]), prompt


def build_agent_2_prompt(row: List[str]) -> str:
    Data_ID = _clean(row[0])
    WVSN_id = _clean(row[1])
    option = int(float(row[2])) if _clean(row[2]) else 0
    WVS_Class = _clean(row[3])
    Cultural_Knowledge_country = _clean(row[4])
    Cultural_Value_country = _clean(row[5])
    agent1 = _clean(row[6])
    agent2 = _clean(row[7])
    agent3 = _clean(row[8])
    Agent_1_Background = _clean(row[9])
    Agent_2_Background = _clean(row[10])
    Agent_3_Background = _clean(row[11])
    Scenario = _clean(row[13])
    Event_1 = _clean(row[14])
    Event_2 = _clean(row[15])
    Agent_1_Goal_1 = _clean(row[18])
    Agent_1_Goal_2 = _clean(row[19])
    Agent_2_Goal_1 = _clean(row[20])
    Agent_2_Goal_2 = _clean(row[21])

    if agent3:
        prompt = f"""
# Task
Act as {agent2} in the scenario and interact with {agent1} to achieve your goal, considering the cultural context in your responses.

# Scenario
{Scenario}

# Events
- Event 1: {Event_1}
- Event 2: {Event_2}

# Characters
- Character 1: {Agent_1_Background}
- Character 2: {Agent_2_Background}
- Character 3: {Agent_3_Background}

# Goals (for you)
- Goal 1: {Agent_2_Goal_1}
- Goal 2: {Agent_2_Goal_2}

# Dialogue Rules
1. Interact with {agent1} to achieve each goal one by one.
2. Keep each round of conversation short and no more than 100 words.
3. Achieve all goals within 20 rounds.
4. Once all goals are achieved, end the dialogue promptly with " GOOD BYE!".
""".strip()
    else:
        prompt = f"""
# Task
Act like {agent2} who has a specific cultural background in the scenario and interact with {agent1} to achieve your goal, considering the cultural context in your responses.

# Scenario
{Scenario}

# Events
- Event 1: {Event_1}
- Event 2: {Event_2}

# Characters
- Character 1: {Agent_1_Background}
- Character 2: {Agent_2_Background}

# Goals (for you)
- Goal 1: {Agent_2_Goal_1}
- Goal 2: {Agent_2_Goal_2}

# Dialogue Rules
1. Interact with {agent1} to achieve each goal one by one.
2. Keep each round of conversation short and no more than 100 words.
3. Achieve all goals within 20 rounds.
4. Once all goals are achieved, end the dialogue promptly with " GOOD BYE!".
""".strip()

    return Data_ID, WVSN_id, option, WVS_Class, Cultural_Knowledge_country, Cultural_Value_country, agent1, agent2, agent3, \
        Agent_1_Background, Agent_2_Background, Agent_3_Background, Scenario, Event_1, Event_2, \
        _clean(row[16]), _clean(row[17]), Agent_1_Goal_1, Agent_1_Goal_2, Agent_2_Goal_1, Agent_2_Goal_2, prompt


def _write_with_header(path: str, rows: List[List[str]]):
    _ensure_dir(path)
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)


def main():
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"Input not found: {INPUT_CSV}")

    with open(INPUT_CSV, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        # Skip header row
        try:
            next(reader)
        except StopIteration:
            raise RuntimeError("Input CSV appears empty (no header row)")

        # Keep non-empty rows only
        data_rows = [row for row in reader if any(_clean(c) for c in row)]

    out_rows_agent1: List[List[str]] = []
    out_rows_agent2: List[List[str]] = []

    for row in data_rows:
        # guard against short rows
        if len(row) < 22:
            # pad with empty strings to required length
            row = list(row) + [""] * (22 - len(row))

        out_rows_agent1.append(list(build_agent_1_prompt(row)))
        out_rows_agent2.append(list(build_agent_2_prompt(row)))

    _write_with_header(OUT_AGENT1, out_rows_agent1)
    _write_with_header(OUT_AGENT2, out_rows_agent2)


if __name__ == "__main__":
    main()
