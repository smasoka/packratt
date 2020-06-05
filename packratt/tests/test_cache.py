# -*- coding: utf-8 -*-
import uuid

import pickle
import pytest

from packratt.cache import cache_factory, CacheEntry, Cache, cache_entry_from_dict
from packratt.google_drive import GoogleDriveCacheEntry
from packratt.url import UrlCacheEntry


class TestCacheEntry(CacheEntry):
    def __init__(self, url, sha_hash, filename):
        self.url = url
        self.sha_hash = sha_hash
        self.filename = filename

    def __eq__(self, other):
        return (self.type == other.type and
                self.url == other.url and
                self.sha_hash == other.sha_hash and
                self.filename == other.filename)

    @property
    def type(self):
        return "test"

    def download(self, destination):
        filename = destination / self.filename

        with open(filename, "w") as f:
            f.write("test")

        return True


def test_cache_multiton(tmp_path_factory):
    cache_dir = tmp_path_factory.mktemp("cache")
    cache_dir2 = tmp_path_factory.mktemp("cache2")
    # Test that we get the same object when creating with the same cache_dir
    assert Cache(cache_dir) is Cache(cache_dir)

    # Test that we get the same object when unpickling with the same cache_dir
    assert pickle.loads(pickle.dumps(Cache(cache_dir))) is Cache(cache_dir)

    # Sanity check
    assert Cache(cache_dir) is not Cache(cache_dir2)


def test_cache(tmp_path_factory):
    cache = cache_factory(tmp_path_factory.mktemp("cache"))

    key = "/ms/wsrt/wst/ms.tar.gz"
    entry = {"url": "ftp://elwood.ru.ac.za/pub/sjperkins/wsrt.ms.tar.gz",
             "hash": uuid.uuid4().hex,
             "filename": "wsrt.ms.tar.gz"}

    cache[key] = entry
    cmp_entry = entry.copy()
    cmp_entry['dir'] = cache.cache_dir / cache.key_dir(key)
    cmp_entry['size'] = 0

    assert cmp_entry == cache[key]

@pytest.mark.parametrize("dict_entry, entry", [
    ({
        "type": "google",
        "file_id": "123456",
        "hash": "123456",
        "filename": "wsrt.ms"
    },
    GoogleDriveCacheEntry("123456", "123456", "wsrt.ms")),
    ({
        "type": "url",
        "url": "https://some.url/somewhere",
        "hash": "123456",
        "filename": "wsrt.ms"
    },
    UrlCacheEntry("https://some.url/somewhere", "123456", "wsrt.ms")),
])
def test_cache_entry_from_dict(dict_entry, entry):
    assert cache_entry_from_dict(dict_entry) == entry


@pytest.mark.skip
def test_google_download(tmp_path_factory):
    dest_dir = tmp_path_factory.mktemp("dest")

    entry = GoogleDriveCacheEntry("1yxDIXUo3Xun9WXxA0x_hvX9Fmxo9Igpr", 0,
                                  "1519747221.subset.ms.tar.gz")

    entry.download(dest_dir)