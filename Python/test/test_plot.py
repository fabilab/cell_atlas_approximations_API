import pytest
import pandas as pd
import unittest

import atlasapprox as aa


class TestPlot(unittest.TestCase):
    def test_import(self):
        try:
            from atlasapprox import pl
        except ImportError:
            pl = None
        self.assertIsNot(pl, None)

        try:
            pl = aa.pl
        except:
            pl = None
        self.assertIsNot(pl, None)

    def test_find_functions(self):
        for name in dir(aa.pl):
            if name in ["average", "dotplot"]:
                obj = getattr(aa.pl, name)
                self.assertTrue(callable(obj))
