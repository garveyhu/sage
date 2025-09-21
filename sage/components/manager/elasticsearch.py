from elasticsearch import Elasticsearch

from sage.complex.config.inventory import ESSettings


class ElasticsearchManager:
    _pool = None

    @classmethod
    def initialize_pool(cls):
        if cls._pool is None:
            if ESSettings.TYPE == "cloud":
                es_cloud_url = ESSettings.CLOUD_URL
                es_api_key = ESSettings.API_KEY
                if es_cloud_url and es_api_key:
                    cls._pool = Elasticsearch(es_cloud_url, api_key=es_api_key)
            elif ESSettings.TYPE == "host":
                es_host_url = ESSettings.HOST_URL
                es_username = ESSettings.USERNAME
                es_password = ESSettings.PASSWORD
                if es_username and es_password:
                    cls._pool = Elasticsearch(
                        es_host_url, http_auth=(es_username, es_password)
                    )
                else:
                    cls._pool = Elasticsearch(es_host_url)

    def __init__(self):
        self.__class__.initialize_pool()
        self.client = self.__class__._pool
