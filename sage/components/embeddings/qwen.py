from langchain_community.embeddings import (
    DashScopeEmbeddings as BaseDashScopeEmbeddings,
)

from sage.complex.config.inventory import case_embedding, keys_qwen


class DashScopeEmbeddings(BaseDashScopeEmbeddings):
    def __init__(self):
        model = case_embedding()
        api_key = keys_qwen()
        super().__init__(model=model, dashscope_api_key=api_key)
