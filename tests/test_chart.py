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
    process = mocker.MagicMock()
    mocker.patch("helmsman.chart.Popen", return_value=process)
    process.poll.return_value = 0
    process.communicate.return_value = (yaml.safe_dump(rendered_yaml), "")

    chart = Chart(faker.color())
    result = chart.render({})
    my_crd = result.where(lambda x: x["kind"] == rendered_yaml["kind"]).single()
    assert my_crd["apiVersion"] == rendered_yaml["apiVersion"]
