import pytest
from helmsman.kind import KindFilter


@pytest.fixture
def resource(faker):
    return {
        "apiVersion": "v1",
        "kind": "MyCrd",
        "metadata": {
            "name": faker.color(),
            "namespace": faker.color(),
            "labels": {
                "app": faker.color(),
                "version": faker.color(),
            },
        },
        "spec": {},
    }


def test_name(resource):
    kind = KindFilter("MyCrd")
    assert kind.name(resource["metadata"]["name"])(resource)
