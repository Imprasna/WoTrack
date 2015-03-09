import pylibmc


class Cache(object):
    _memcached = None

    @classmethod
    def memcached_handle(cls):
        """
        :return: the Singleton handle to the memcache server
        """
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
        """
        :param key: memcache key for the object
        :return: the object from cache if it exists
        """
        return cls.memcached_handle().get(key)

    @classmethod
    def set(cls, key, object_to_cache):
        """
        :param key: random key to be used as the object's memcache key
        :param object_to_cache: the object to put into the cache
        """
        cls.memcached_handle()[key] = object_to_cache

    @classmethod
    def clear(cls):
        """
        Flushes the cache. All Objects in cache are destroyed
        """
        cls.memcached_handle().flush_all()