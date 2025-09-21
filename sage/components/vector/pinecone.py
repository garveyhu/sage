from langchain_pinecone import PineconeVectorStore

from sage.complex.config.inventory import keys_pinecone
from sage.components.inventory import embedding


class PineconeVector:
    """Pinecone存储向量（向量化）."""

    def __init__(self):
        self.api_key = keys_pinecone()
        self.embedding = embedding()

    def pinecone_vector(self):
        """会话向量Store"""
        return PineconeVectorStore(
            pinecone_api_key=self.api_key,
            embedding=self.embedding,
            index_name="langchain",
        )
