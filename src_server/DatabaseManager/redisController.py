import redis

class RedisController:
    def __init__(self) -> None:
        self.red = redis.Redis(host='localhost', port=6379, db=0)
