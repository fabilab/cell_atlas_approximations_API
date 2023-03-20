import pytest
import requests


def test_features(host):
    response = requests.get(
        f"{host}/features",
        params={"organism": "h_sapiens"},
    )
    resp_content = response.json()

    assert list(resp_content.keys()) == ["organism", "features"]
    assert resp_content["organism"] == "h_sapiens"
    assert len(resp_content["features"]) > 10000
