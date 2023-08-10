from redis import Redis

import settings


class BaseRedis:
    def __init__(self, db: int, expire_time):
        self.redis_connection = Redis(host=settings.REDIS_URL, port=settings.REDIS_PORT, db=db)
        self.expire_time = expire_time

    def set(self, name, value):
        self.redis_connection.set(name, value, self.expire_time)

    def get(self, name):
        self.redis_connection.get(name)

    def delete(self, name):
        self.redis_connection.delete(name)


class RedisSession(BaseRedis):
    def __init__(self):
        db = 0
        expire_time = settings.AUTHORIZATION_EXPIRE_TIME  # 30 days
        super(RedisSession, self).__init__(db, expire_time)
