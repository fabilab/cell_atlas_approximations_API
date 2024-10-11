import pytest
import pandas as pd
import unittest

import atlasapprox as aa


class TestBasic(unittest.TestCase):
    def test_init(self):
        api = aa.API()

    def test_average(self):
        api = aa.API()
        res = api.average(
            organism="h_sapiens",
            organ="lung",
            features=["CD4", "CD8A"],
        )

        self.assertEqual(type(res), pd.DataFrame)
        self.assertEqual(res.shape[0], 2)
        self.assertEqual(res.index.tolist(), ["CD4", "CD8A"])
        self.assertTrue((res.values >= 0).all())

    def test_dotplot(self):
        api = aa.API()
        res = api.dotplot(
            organism="h_sapiens",
            organ="lung",
            features=["CD4", "CD8A"],
        )
        self.assertEqual(type(res), dict)

        avg = res["average"]
        self.assertEqual(type(avg), pd.DataFrame)
        self.assertEqual(avg.shape[0], 2)
        self.assertEqual(avg.index.tolist(), ["CD4", "CD8A"])
        self.assertTrue((avg.values >= 0).all())
