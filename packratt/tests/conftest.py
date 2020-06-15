from packratt.cache import get_cache, set_cache, Cache
from packratt.registry import load_registry

import pytest
import yaml


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
'/test/ms/2020-06-04/google/smallest_ms.tar.gz':
  file_id: 1wjZoh7OAIVEjYuTmg9dLAFiLoyehnIcL
  hash: 4d548b22331fb3cd3256b1b4f37a41cf
  description: >
    Small testing Measurement Set, stored on Google Drive
'''


@pytest.fixture(scope="session")
def registry(tmp_path_factory):

    user_conf_path = tmp_path_factory.mktemp("conf")
    USER_REGISTRY = user_conf_path / "registry.yaml"
    CONTENT = yaml.dump(content)
    USER_REGISTRY.write_text(CONTENT)
    assert USER_REGISTRY.read_text() == CONTENT

    return load_registry()
