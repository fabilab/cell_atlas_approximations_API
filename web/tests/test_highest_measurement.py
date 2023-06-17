import pytest
import requests


def test_markers(host):
    response = requests.get(
        f"{host}/highest_measurement",
        params={
            "organism": "m_musculus",
            "feature": "Col1a1",
            "number": 3,
        },
    )
    resp_content = response.json()

    assert list(resp_content.keys()) == [
            "organism", "feature", "organs", "celltypes", "average", "unit"]
    assert resp_content["organism"] == "m_musculus"
    assert resp_content["feature"] == "Col1a1"
    assert len(resp_content["organs"]) == len(resp_content["celltypes"]) == 3
