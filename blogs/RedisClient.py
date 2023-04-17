import redis
class RedisClient:
    # r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r = redis.cluster.RedisCluster(host='demo-redis.idddlr.clustercfg.aps1.cache.amazonaws.com', port=6379)
    
    def __init__(self): 
        pass

    @staticmethod
    def is_cached(key):
        return RedisClient.r.exists(key)

    @staticmethod
    def get_cache(key):
        if(RedisClient.r.exists(key) == False):
            return None
        return RedisClient.r.get(key)
    
    @staticmethod
    def cache(key, data):
        # print(data)
        RedisClient.r.set(key, data)
        