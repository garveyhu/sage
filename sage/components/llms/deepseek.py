from langchain_deepseek import ChatDeepSeek as BaseChatDeepSeek

from sage.complex.config.inventory import keys_deepseek, case_llm, llm_temperature


class ChatDeepSeek(BaseChatDeepSeek):
    def __init__(self):
        model = case_llm()
        api_key = keys_deepseek()
        temperature = llm_temperature()
        super().__init__(model=model, api_key=api_key, temperature=temperature)
