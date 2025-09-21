from sage.complex.config.inventory import case_embedding
from sage.components.embeddings.openai import OpenAIEmbeddings
from sage.components.embeddings.qwen import DashScopeEmbeddings


class EmbeddingFactory:
    embeddings = {
        "text-embedding-3-large": OpenAIEmbeddings,
        "text-embedding-3-small": OpenAIEmbeddings,
        "text-embedding-v4": DashScopeEmbeddings,
    }

    @classmethod
    def create_embedding(cls, embedding_type=None):
        if embedding_type is None:
            embedding_type = case_embedding()

        embedding_class = cls.embeddings.get(embedding_type)
        if not embedding_class:
            raise ValueError(f"No embedding class found for type {embedding_type}")

        return embedding_class()
