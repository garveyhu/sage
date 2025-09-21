from langchain_openai import OpenAIEmbeddings as BaseOpenAIEmbeddings

from sage.complex.config.inventory import (
    case_embedding,
    embedding_dimensions,
    keys_openai,
)


class OpenAIEmbeddings(BaseOpenAIEmbeddings):
    def __init__(self):
        model = case_embedding()
        api_key = keys_openai()
        dimensions = embedding_dimensions()
        super().__init__(model=model, api_key=api_key, dimensions=dimensions)
