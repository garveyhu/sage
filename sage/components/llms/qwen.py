from langchain_qwq import ChatQwen as BaseChatQwen

from sage.complex.config.inventory import keys_qwen, case_llm, llm_temperature


class ChatQwen(BaseChatQwen):
    def __init__(self):
        model = case_llm()
        api_key = keys_qwen()
        temperature = llm_temperature()
        super().__init__(model=model, api_key=api_key, temperature=temperature)
