from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.core.config import settings


class CacheManager:
    def __init__(self, host: str, port: int, db: int, prefix_redis: str):
        self.host = host
        self.port = port
        self.db = db
        self.prefix_redis = prefix_redis
        self.redis_client = None

    async def init_cache(self):
        """
        Initialize the Redis cache.
        """
        self.redis_client = aioredis.Redis(host=self.host, port=self.port, db=self.db)
        FastAPICache.init(RedisBackend(self.redis_client), prefix=self.prefix_redis)

    @classmethod
    async def close_cache(cls):
        backend = FastAPICache.get_backend()
        if isinstance(backend, RedisBackend):
            redis = backend.redis
            await redis.close()

    @classmethod
    async def set_cache_value(cls, key: str, value: bytes, expire: int = None):
        """
        Set a value in the Redis cache.
        """
        backend = FastAPICache.get_backend()
        await backend.set(key, value, expire=expire)

    @classmethod
    async def get_cache_value(cls, key: str):
        """
        Get a value from the Redis cache.
        """
        backend = FastAPICache.get_backend()
        return await backend.get(key)


cache_manager = CacheManager(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    prefix_redis=settings.redis_prefix,
)
