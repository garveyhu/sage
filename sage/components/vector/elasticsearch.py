from langchain_elasticsearch import ElasticsearchStore

from sage.complex.config.inventory import dialog_id
from sage.components.embeddings.embedding_factory import EmbeddingFactory
from sage.components.manager.elasticsearch import ElasticsearchManager


class ElasticsearchVector:
    """Elasticsearch存储向量（向量化）."""

    def __init__(self):
        self.client = ElasticsearchManager().client
        self.embedding = EmbeddingFactory.create_embedding()

    def dialog_vector(self):
        """会话向量Store"""
        return ElasticsearchStore(
            es_connection=self.client,
            embedding=self.embedding,
            index_name="dialog_" + dialog_id(),
        )

    def resource_vector(self):
        """资源向量Store"""
        return ElasticsearchStore(
            es_connection=self.client,
            embedding=self.embedding,
            index_name="resource_" + dialog_id(),
        )
