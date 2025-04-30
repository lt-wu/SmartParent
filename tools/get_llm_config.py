import autogen

def get_llm_config(model_name):
    return {
        "config_list": autogen.config_list_from_json("OAI_CONFIG_LIST", filter_dict={"model": [model_name]}),
        "cache_seed": 41,
    }
