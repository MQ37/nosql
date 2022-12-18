import redis

MONGODB_SETTINGS = {
    "username": "root",
    "password": "toor",
    "db": "webapp",
    "host": "localhost",
    "port": 27017,
    "alias": "default",
}
SESSION_TYPE = "redis"
SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
