import pytest
import requests


def test_organisms(host):
    response = requests.get(f"{host}/organisms")
    resp_content = response.json()

    assert list(resp_content.keys()) == ["organisms"]
    assert len(resp_content["organisms"]) > 4
