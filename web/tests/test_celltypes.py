import pytest
import requests


def test_celltypes(host):
    response = requests.get(
        f"{host}/celltypes",
        params={
            "organism": "h_sapiens",
            "organ": "Lung",
        },
    )
    resp_content = response.json()

    assert list(resp_content.keys()) == ["organism", "organ", "celltypes"]
    assert resp_content["organism"] == "h_sapiens"
    assert resp_content["organ"] == "Lung"
    assert "fibroblast" in resp_content["celltypes"]
