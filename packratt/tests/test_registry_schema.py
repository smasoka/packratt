from pathlib import Path

from jsonschema import validate
import yaml

from packratt.registry import REGISTRY_SCHEMA

def test_schema():
    validate(
    {
        "/ms/vla/vla012345.ms" : {
            "type": "url",
            "url": "https://blah.org/vla012345.ms",
            "hash": "123456",
            "filename": "vla012345.ms",
        },
        "/ms/vla/vla543210.ms" : {
            "type": "google",
            "file_id": "123456",
            "hash": "123456",
            "filename": "vla012345.ms",
        },
    },
    schema=REGISTRY_SCHEMA)