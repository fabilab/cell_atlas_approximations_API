import pytest
import requests


def test_markers(host):
    response = requests.get(
        f"{host}/markers",
        params={
            "organism": "m_musculus",
            "organ": "Lung",
            "celltype": "fibroblast",
            "number": 3,
        },
    )
    resp_content = response.json()

    assert list(resp_content.keys()) == [
            "organism", "organ", "celltype", "markers"]
    assert resp_content["organism"] == "m_musculus"
    assert resp_content["organ"] == "Lung"
    assert resp_content["celltype"] == "fibroblast"
    # FIXME: THESE ARE MARKERS FOR ASM, CHECK THE DATA
    assert resp_content["markers"] == ["Hhip", "Aspn", "Grem2"]
