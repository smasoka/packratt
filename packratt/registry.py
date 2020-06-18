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


USER_REGISTRY = Path(user_config_dir, "registry.yaml")


def load_user_registry():
    with open(USER_REGISTRY, "r") as f:
        registry = yaml.safe_load(f)

    validate(registry, schema=REGISTRY_SCHEMA)

    return registry


def load_default_registry():
    path = Path(Path(packratt.__file__).parent, "conf", "registry.yaml")

    with open(path, "r") as f:
        registry = yaml.safe_load(f)

    validate(registry, schema=REGISTRY_SCHEMA)

    return registry


def load_registry(filename=None):

    if filename is None:
        registry = load_default_registry()

    if USER_REGISTRY.is_file():
        registry.update(load_user_registry())

    return registry
