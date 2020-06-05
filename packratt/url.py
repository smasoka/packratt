# -*- coding: utf-8 -*-
from pathlib import Path
import requests

from packratt.cache import CacheEntry

class UrlCacheEntry(CacheEntry):
    def __init__(self, url, sha_hash, filename):
        self.url = url
        self.sha_hash = sha_hash
        self.filename = filename

    def download(self, destination: Path) -> bool:
        CHUNK_SIZE = 2**20
        filename = destination / self.filename

        with requests.Session() as session:
            with session.get(self.url, stream=True) as response:
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(CHUNK_SIZE):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
        return True

    @property
    def type(self):
        return "url"

    def __eq__(self, other):
        return (self.type == other.type and
                self.url == other.url and
                self.sha_hash == other.sha_hash and
                self.filename == other.filename)


    def __hash__(self):
        return hash(self.url, self.sha_hash, self.filename)