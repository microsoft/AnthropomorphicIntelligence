# Mapping from data sources to evaluation metrics
DATASOURCE_METRICS = {
    # MSS Wiki dataset
    'mss/wiki': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'semantic_similarity',
        'metrics': ['format', 'em', 'subem', 'llm']
    },
    # Other MSS datasets
    'mss': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'semantic_similarity',
        'metrics': ['format', 'em', 'subem', 'llm']
    },
    'subem': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'semantic_similarity',
        'metrics': ['subem'] 
    },
     # Social Reasoning datasets
    'social/human_sr': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_reasoning',
        'metrics': ['format', 'llm']
    },
    'social/qa': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_reasoning',
        'metrics': ['format', 'llm']
    },
    'social/mc': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'semantic_similarity',
        'metrics': ['format', 'llm']
    },
    'cpdc/toolcall': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'roleplay',
        'metrics': ['toolcall_f1']
    },
    'cpdc/roleplay': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'roleplay',
        'metrics': ['llm']
    },
    'ki': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'semantic_similarity_keep_think',
        'metrics': ['llm']
    },
    'searchR1_nq': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'semantic_similarity',
        'metrics': ['llm', 'em', 'subem']
    },
    'socialR0': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_r0',
        'metrics': [ 'format', 'em'] # this is for social-r1 project
    },
    'socialR1': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_r1',
        'metrics': ['llm', 'format', 'em']  
    },
    'socialR2': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_r2',
        'metrics': ['llm', 'format', 'em']
    },
    'socialR3': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_r3',
        'metrics': ['llm', 'format', 'em']
    },
    'socialR4': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_r4',
        'metrics': ['llm', 'format', 'em']
    },
    'socialR5': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_r5',
        'metrics': ['llm', 'format', 'em','rm']
    },
    'ToM-RL': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'tom_rl',
        'metrics': ['em', 'format']
    },
    'conversation': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'conversation',
        'metrics': ['llm', 'format', 'llm_outcome']
    },
    'writing': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'writing',
        'metrics': ['llm', 'format', 'llm_outcome']
    },
    'social_qa': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'social_qa',
        'metrics': ['llm', 'format', 'llm_outcome']
    },
    'persona': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'persona',
        'metrics': ['llm', 'format', 'llm_outcome']
    },
    'socsci': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'socsci',
        'metrics': ['llm', 'format', 'em']
    },
    'item_selection': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'item_selection',
        'metrics': ['llm', 'format', 'em']
    },
    'socialr1': {
        'llm_module': 'llm_evaluate',
        'llm_mode': 'socialr1',
        'metrics': ['llm', 'format', 'em']  # this is for human llm project
    }, 
}