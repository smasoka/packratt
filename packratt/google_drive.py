# -*- coding: utf-8 -*-
from pathlib import Path

import requests

from packratt.cache import CacheEntry

URL = "https://drive.google.com/uc?export=download"


class GoogleDriveCacheEntry(CacheEntry):
    def __init__(self, file_id, sha_hash, filename):
        self.file_id = file_id
        self.sha_hash = sha_hash
        self.filename = filename

    @staticmethod
    def _get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    @property
    def type(self):
        return "google"

    def __eq__(self, other):
        return (self.type == other.type and
                self.file_id == other.file_id and
                self.sha_hash == other.sha_hash and
                self.filename == other.filename)


    def download(self, destination: Path) -> bool:
        CHUNK_SIZE = 2**20
        filename = destination / self.filename

        with requests.Session() as session:
            try:
                params = {'id': self.file_id}
                response = session.get(URL, params=params, stream=True)
                token = self._get_confirm_token(response)

                # Implies a long response, re-request with confirmation token
                if token:
                    response.close()
                    params = {'id': self.file_id, 'confirm': token}
                    response = session.get(URL, params=params, stream=True)

                with open(filename, "wb") as f:
                    for chunk in response.iter_content(CHUNK_SIZE):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
            finally:
                response.close()

        return True

    def __hash__(self):
        return hash(self.file_id, self.sha_hash, self.filename)