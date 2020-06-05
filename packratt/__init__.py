__version__ = '0.1.0'


cache = None


def get(key, default=None):
    global cache

    # Get the cache
    if cache is None:
        from packratt.cache import cache_factory
        cache = cache_factory()

    if default is None:
        try:
            return cache[key]
        except KeyError:
            raise ValueError("%s is not registered")
    elif isinstance(default, dict):
        from packaging.cache import cache_entry_from_dict
        return cache.get(key, cache_entry_from_dict(default))
    else:
        raise TypeError("default must be None or dict")
