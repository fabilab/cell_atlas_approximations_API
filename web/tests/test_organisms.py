import pytest
import requests


def test_organisms(host):
    response = requests.get(f"{host}/organisms")
    resp_content = response.json()

    assert list(resp_content.keys()) == ["organisms"]
    assert sorted(resp_content["organisms"]) == [
        "c_elegans",
        "d_rerio",
        "h_sapiens",
        "m_musculus",
        "m_myoxinus",
    ]
