import pytest
import unittest
import requests


url = "https://api.atlasapprox.org/v1/"


class TestBasic(unittest.TestCase):
    def test_average(self):
        res = requests.get(
            url + "average",
            params=dict(
                organism="h_sapiens",
                organ="lung",
                features=["CD4", "CD8A"],
            ),
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["Content-Type"], "application/json")
        res = res.json()
        self.assertEqual(type(res), dict)
