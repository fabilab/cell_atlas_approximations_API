import pytest
import requests


def test_celltypes(host):
    response = requests.get(
        f"{host}/celltypexorgan",
        params={
            "organism": "h_sapiens",
        },
    )
    resp_content = response.json()

    assert list(resp_content.keys()) == ["organism", "organs", "celltypes", "detected"]
    assert resp_content["organism"] == "h_sapiens"
    assert len(resp_content["organs"]) > 4
    assert "fibroblast" in resp_content["celltypes"]
