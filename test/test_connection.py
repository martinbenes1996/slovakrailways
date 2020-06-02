import re
import sys
import unittest
import warnings

sys.path.append(".")

import slovakrailways as zsr

class TestConnection(unittest.TestCase):
    def setUp(self):
        pass
    def test_departures(self):
        deps = zsr.Connection.departures(uic_code = "5613206")
        