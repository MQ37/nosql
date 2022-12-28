import os
import redis

MONGODB_SETTINGS = {
    "username": os.getenv("mongo_user", "root"),
    "password": os.getenv("mongo_pass", "toor"),
    "db": "webapp",
    "host": os.getenv("mongo_host", "localhost"),
    "port": os.getenv("mongo_port", 27017),
    "alias": "default",
}
SESSION_TYPE = "redis"
SESSION_REDIS = redis.from_url("redis://%s:6379" %
                               os.getenv("redis_host", "127.0.0.1"))
NEO4J_HOST = os.getenv("neo4j_host", "127.0.0.1")
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "mypassword"
