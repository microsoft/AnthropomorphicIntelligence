

echo "==== Step 1: Data Preprocess ===="
cd "$(dirname "$0")/data"
python data_preprocess.py
cd ..

echo "==== Step 2: Generate Dialogue (open model) ===="
# Please make sure setting azure in function build_clients_and_configs 
# using openai key 
python gen_open_model.py --agent2_model llama2:7b-chat


echo "==== Step 3: Clean Dialogue ===="
python clean_closed_model.py --agent2_model llama2:7b-chat

echo "==== Step 4: Evaluate Dialogue ===="
# Please make sure setting azure in function call_llm 
python eva_closed_model_azure.py --agent2_model llama2:7b-chat --judge_model gpt-4o
# Please make sure setting azure in function call_llm 
# using openai key 
# python gen_closed_model_key.py --agent2_model gpt-4.1

echo "==== Step 5: Get Final Result ===="
python get_result.py --agent2_model llama2:7b-chat

echo "==== All Done ===="



