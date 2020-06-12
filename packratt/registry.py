# -*- coding: utf-8 -*-

from pathlib import Path

import yaml
from jsonschema import validate

import packratt
from packratt.directories import user_config_dir

SCHEMA_PATH = Path(Path(packratt.__file__).parent,
                   "conf", "registry-schema.yaml")

# Open the schema file
with open(SCHEMA_PATH, "r") as f:
    SCHEMA = yaml.safe_load(f)

# Create registry and entry schemas
REGISTRY_SCHEMA = {**SCHEMA, "$ref": "#/definitions/registry"}
ENTRY_SCHEMA = {**SCHEMA, "entry": {"type": {"$ref": "/definitions/entry"}}}

del SCHEMA_PATH


def load_registry(filename=None):

    if filename is None:

        path = Path(Path(packratt.__file__).parent,
                    "conf", "registry.yaml")

        user_path = Path(user_config_dir, "registry.yaml")

        if user_path.is_file():
            path = user_path

    with open(path, "r") as f:
        registry = yaml.safe_load(f)

    validate(registry, schema=REGISTRY_SCHEMA)

    return registry
