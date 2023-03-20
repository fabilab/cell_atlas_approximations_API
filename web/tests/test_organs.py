import pytest
import requests


def test_organs(host):
    response = requests.get(
        f"{host}/organs",
        params={"organism": "h_sapiens"},
    )
    resp_content = response.json()

    assert list(resp_content.keys()) == ["organism", "organs"]
    assert resp_content["organism"] == "h_sapiens"
    assert len(resp_content["organs"]) > 3
