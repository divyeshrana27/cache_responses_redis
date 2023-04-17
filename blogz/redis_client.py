from redis.cluster import RedisCluster
from django_redis.client import DefaultClient

class CustomRedisCluster(DefaultClient):
    def connect(self, index: int = 0):
        return RedisCluster.from_url(self._server[index])