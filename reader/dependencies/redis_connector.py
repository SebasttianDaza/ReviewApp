from redis.sentinel import Sentinel
from redis import StrictRedis
from reader.config import get_settings

settings = get_settings()

SENTINEL_HOSTS = [(settings.redis_cache_host_reader, settings.redis_cache_port_reader)]
MASTER_NAME = settings.redis_cache_master_node_reader

def get_redis_connection() -> tuple[StrictRedis, StrictRedis]:
    try:
        sentinel = Sentinel(
            SENTINEL_HOSTS,
            socket_timeout=0.1,
            password=settings.redis_cache_password_reader,
        )

        master_conn = sentinel.master_for(MASTER_NAME, socket_timeout=0.1, password=settings.redis_cache_password_reader)
        replica_conn = sentinel.slave_for(MASTER_NAME, socket_timeout=0.1, password=settings.redis_cache_password_reader)


        if master_conn.ping():
            print(f"DEBUG: Master PING OK. Host: {master_conn.connection_pool.connection_kwargs.get('host')}")
        else:
            raise ConnectionError("Master failed PING after connection.")
        return master_conn, replica_conn
    except Exception as e:  
        print(f"Error connecting to Redis: {e}")
        raise ConnectionError("Could not connect to Redis")
