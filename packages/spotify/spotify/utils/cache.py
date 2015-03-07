import pylibmc


class Cache(object):
    _memcached = None

    @classmethod
    def memcached_handle(cls):
        if not cls._memcached:
            try:
                cls._memcached = pylibmc.Client(
                    ["127.0.0.1"],
                    binary=True,
                    behaviors={
                        "tcp_nodelay": True,
                        "ketama": True
                    }
                )
            except Exception:
                return None

        return cls._memcached

    @classmethod
    def get(cls, key):
        return cls.memcached_handle().get(key)

    @classmethod
    def set(cls, key, object_to_cache):
        cls.memcached_handle()[key] = object_to_cache

    @classmethod
    def clear(cls):
        cls.memcached_handle().flush_all()