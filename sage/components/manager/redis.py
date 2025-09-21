from redis import ConnectionPool, Redis, Sentinel, SentinelConnectionPool

from sage.complex.config.inventory import RedisSettings


class RedisManager:
    _pool = None

    @classmethod
    def initialize_pool(cls):
        if cls._pool is None:
            if RedisSettings.SENTINEL_MASTER:
                sentinel = Sentinel(
                    [(RedisSettings.HOST, RedisSettings.PORT)],
                    socket_timeout=RedisSettings.TIMEOUT,
                    sentinel_kwargs={"password": RedisSettings.SENTINEL_PASSWORD},
                )
                cls._pool = SentinelConnectionPool(
                    master_name=RedisSettings.SENTINEL_MASTER,
                    sentinel_manager=sentinel,
                    socket_timeout=RedisSettings.TIMEOUT,
                    password=RedisSettings.PASSWORD,
                    db=RedisSettings.DB,
                )
            else:
                cls._pool = ConnectionPool(
                    host=RedisSettings.HOST,
                    port=RedisSettings.PORT,
                    db=RedisSettings.DB,
                    password=RedisSettings.PASSWORD,
                )

    def __init__(self):
        self.__class__.initialize_pool()
        self.client = Redis(connection_pool=self.__class__._pool)
