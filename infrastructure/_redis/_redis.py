import redis.commands.json
from redis import Redis


class _Redis:
    def __init__(self, host: str, port: int, db: int):
        self.host = host
        self.port = port
        self.db = db

        self.redis = Redis(host=host, port=port, db=db)

    def set(self, key: str, value: str):
        self.redis.set(key, value)

    def get(self, key: str):
        value = self.redis.get(key)

        if isinstance(value, bytes):
            return value.decode("utf-8")

        return value

    def delete(self, key: str):
        self.redis.delete(key)
