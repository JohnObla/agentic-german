from autogen import LLMConfig

def make_llm_config(response_format):
    return LLMConfig(
        api_type="openai",
        model="gpt-4o-mini",
        temperature=0.2,
        response_format=response_format,
    ) 