from packratt.cache import get_cache, set_cache, Cache
from packratt.registry import load_registry, load_user_registry
from packratt.directories import user_config_dir

from unittest.mock import patch, mock_open
import pytest
import yaml

from pathlib import Path


@pytest.fixture(scope="session", autouse=True)
def global_test_cache(tmp_path_factory):
    cache_dir = tmp_path_factory.mktemp('cache')
    set_cache(Cache(cache_dir))


@pytest.fixture
def test_cache(tmp_path_factory):
    cache_dir = tmp_path_factory.mktemp('cache')

    old_cache = get_cache()

    try:
        new_cache = Cache(cache_dir)
        set_cache(new_cache)
        yield new_cache
    finally:
        set_cache(old_cache)


content = '''\
'/test/ms/2020-06-04/google/test_ms.tar.gz':
  type: google
  file_id: 1wjZoh7OAIVEjYuTmg9dLAFiLoyehnIcL
  hash: 4d548b22331fb3cd3256b1b4f37a41cf
  description: >
    Small testing Measurement Set, stored on Google Drive
'''


@pytest.fixture(scope="session", autouse=True)
def user_registry():
    CONTENT = yaml.safe_load(content)
    USER_REGISTRY = Path(user_config_dir, "registry.yaml")

    with patch('builtins.open', new_callable=mock_open(read_data=content))\
            as m:
        with patch('yaml.safe_load', return_value=CONTENT):
            reg = load_user_registry()

    m.assert_called_with(USER_REGISTRY, 'r')
    assert reg == CONTENT


@pytest.fixture(scope="session")
def registry(tmp_path_factory):

    return load_registry()
