import pytest

from helmsman.chart import Chart
import yaml


@pytest.fixture
def rendered_yaml(faker):
    return {
        "apiVersion": "v1",
        "kind": "MyCrd",
        "spec": {},
    }


def test_render(faker, mocker, rendered_yaml):
    command = mocker.MagicMock(return_code=0, out=yaml.safe_dump(rendered_yaml), err="")
    mocker.patch("helmsman.chart.run", return_value=command)

    chart = Chart(faker.color())
    result = chart.render({})
    assert (
        result.where(lambda x: x["kind"] == rendered_yaml["kind"])
        .select(lambda x: x["apiVersion"])
        .first()
        == rendered_yaml["apiVersion"]
    )
