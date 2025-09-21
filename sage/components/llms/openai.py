from langchain_openai import ChatOpenAI as BaseChatOpenAI

from sage.complex.config.inventory import keys_openai, case_llm, llm_temperature


class ChatOpenAI(BaseChatOpenAI):
    def __init__(self):
        model = case_llm()
        api_key = keys_openai()
        temperature = llm_temperature()
        super().__init__(model=model, openai_api_key=api_key, temperature=temperature)
