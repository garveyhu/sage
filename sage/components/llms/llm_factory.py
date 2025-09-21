from sage.complex.config.inventory import case_llm
from sage.components.llms.deepseek import ChatDeepSeek
from sage.components.llms.openai import ChatOpenAI
from sage.components.llms.qwen import ChatQwen


class LLMFactory:
    llms = {
        "gpt-5": ChatOpenAI,
        "gpt-5-mini": ChatOpenAI,
        "gpt-5-nano": ChatOpenAI,
        "deepseek-chat": ChatDeepSeek,
        "deepseek-reasoner": ChatDeepSeek,
        "qwen3-max-preview": ChatQwen,
        "qwen-plus": ChatQwen,
        "qwen-flash": ChatQwen,
    }

    @classmethod
    def create_llm(cls, llm_type=None):
        if llm_type is None:
            llm_type = case_llm()

        llm_class = cls.llms.get(llm_type)
        if not llm_class:
            raise ValueError(f"No llm class found for type {llm_type}")

        return llm_class()
