import pytest
import requests


def test_fraction_detected(host):
    response = requests.get(
        f"{host}/fraction_detected",
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
        "fraction_detected",
        "celltypes",
        "unit",
    ]
    assert resp_content["organism"] == "h_sapiens"
    assert resp_content["organ"] == "Lung"
    assert resp_content["features"] == ["COL1A1", "PTPRC"]
    assert len(resp_content["fraction_detected"]) == 2
    assert len(resp_content["fraction_detected"][0]) > 8
