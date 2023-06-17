import pytest
import requests


def test_average(host):
    response = requests.get(
        f"{host}/average",
        params={
            "organism": "h_sapiens",
            "organ": "Lung",
            "features": ",".join(["COL1A1", "PTPRC"]),
        },
    )
    resp_content = response.json()

    assert list(resp_content.keys()) == [
        "organism",
        "organ",
        "features",
        "average",
        "celltypes",
        "unit",
    ]
    assert resp_content["organism"] == "h_sapiens"
    assert resp_content["organ"] == "Lung"
    assert resp_content["features"] == ["COL1A1", "PTPRC"]
    assert len(resp_content["average"]) == 2
    assert len(resp_content["average"][0]) > 8
