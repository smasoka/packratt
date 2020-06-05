# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from hashlib import sha224
from pathlib import Path
from threading import Lock
import weakref

from jsonschema import validate, ValidationError
import yaml

from packratt.registry import load_registry, SCHEMA

ENTRY_SCHEMA = {**SCHEMA, "entry": {"type": {"$ref": "/definitions/entry"}}}

class CacheEntry(metaclass=ABCMeta):
    @abstractmethod
    def download(self, destination):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @property
    @abstractmethod
    def type(self):
        pass


_cache_lock = Lock()
_cache_cache = weakref.WeakValueDictionary()

class CacheMetaClass(type):
    """
    https://en.wikipedia.org/wiki/Multiton_pattern

    """
    def __call__(cls, cache_dir):
        with _cache_lock:
            try:
                return _cache_cache[cache_dir]
            except KeyError:
                instance = type.__call__(cls, cache_dir)
                _cache_cache[cache_dir] = instance
                return instance


class Cache(metaclass=CacheMetaClass):
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.registry = load_registry()

    def __reduce__(self):
        return (Cache, (self.cache_dir,))


    @staticmethod
    def key_dir(key) -> Path:
        h = sha224(key.encode('ascii')).hexdigest()
        return Path(h[0:2], h[2:4], h[4:6], h[6:])

    def cache_key_dir(self, key) -> Path:
        """
        Parameters
        ----------
        key : str
            Cache entry key

        Returns:
        path : :class:`Path`
            Path to the cache entry
        """
        return Path(self.cache_dir) / self.key_dir(key)

    def __setitem__(self, key, value):
        """
        Inserts a Cache entry

        Parameters
        ----------
        key : str
            Cache entry key
        value : dict
            Cache entry
        """
        if not isinstance(value, dict):
            raise TypeError("value must be a dict")

        # Is this a valid cache entry dictionary?
        try:
            validate(value, ENTRY_SCHEMA)
        except ValidationError as e:
            raise ValueError("%s is not a valid entry" % value) from e

        entry_dir = self.cache_key_dir(key)

        try:
            entry_dir.mkdir(parents=True, exist_ok=True)
        except FileExistsError as e:
            raise ValueError("Already exists") from e

        with open(entry_dir / "entry.yaml", "w") as f:
            f.write(yaml.safe_dump(value))


    def __getitem__(self, key):
        """
        Retrieves a cache entry

        Parameters
        ----------
        key : str
            Cache entry key

        Returns
        -------
        entry : :class:`CacheEntry`
            Cache entry
        """
        entry_dir = self.cache_key_dir(key)

        # Try obtain the entry from the registry first
        # It's the primary source of truth
        try:
            entry = self.registry[key]
        except KeyError:
            # Look for an entry file as the secondary source of truth
            entry_file = entry_dir / "entry.yaml"

            # Nothing, raise a KeyError
            if not entry_file.exists():
                raise KeyError(key)

            with open(entry_file, "r") as f:
                entry = yaml.safe_load(f)
        else:
            self.__setitem__(key, entry)


        entry['size'] = 0
        entry['dir'] = entry_dir

        return entry


def cache_factory(cache_dir=None):
    if cache_dir is None:
        from packratt.directories import user_cache_dir as cache_dir

    return Cache(cache_dir)


def cache_entry_from_dict(entry):
    try:
        entry_type = entry['type']
    except KeyError:
        raise ValueError("entry dictionary must contain a type key")

    if entry_type == "google":
        from packratt.google_drive import GoogleDriveCacheEntry

        try:
            file_id = entry["file_id"]
            file_hash = entry["hash"]
            filename = entry["filename"]
        except KeyError as e:
            raise ValueError("google entry must contain the following keys: "
                             "file_id, hash, filename. missing %s" % str(e))

        return GoogleDriveCacheEntry(file_id, file_hash, filename)

    elif entry_type == "url":
        from packratt.url import UrlCacheEntry

        try:
            url = entry["url"]
            file_hash = entry["hash"]
            filename = entry["filename"]
        except KeyError as e:
            raise ValueError("url entry must contain the following keys: "
                             "url, hash, filename. missing %s" % str(e))

        return UrlCacheEntry(url, file_hash, filename)

    else:
        raise ValueError("Invalid entry_type %s" % entry_type)