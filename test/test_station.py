
import re
import sys
import unittest
import warnings

sys.path.append(".")

import slovakrailways as zsr

class TestStation(unittest.TestCase):
    def setUp(self):
        pass
    
    def _query_station_regex_keys(self, stations):
        
        for station in stations:
            station = zsr.meta.to_key(station)
            yield f"^.*{station}.*$"
        
        
    def test_list_bratislava(self):
        x = zsr.Station.get("bratislava")
        query_stations = [ i.key() for i in x]

        bratislava_stations = ["bratislava hl.st.", "predmestie", "uns", "lamac",
                               "nove mesto","petrzalka", "raca", "vajnory", "vinohrady"]
        for station_regex in self._query_station_regex_keys(bratislava_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    
    def test_list_kosice(self):
        x = zsr.Station.get("kosice")
        query_stations = [ i.key() for i in x]
        
        for station_regex in self._query_station_regex_keys(["kosice", "predmestie"]):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    
    def test_list_presov(self):
        x = zsr.Station.get("presov")
        query_stations = [ i.key() for i in x]
        
        presov_stations = ["presov","mesto","as mhd","nemocnica j.a.reimana","pri mestskom cintorine","nizna sebastova"]
        for station_regex in self._query_station_regex_keys(presov_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)

    def test_list_zilina(self):
        x = zsr.Station.get("zilina")
        query_stations = [ i.key() for i in x]
        
        zilina_stations = ["zilina","solinky","zariecie"]
        for station_regex in self._query_station_regex_keys(zilina_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)

    def test_lazy_fetch(self):
        x = zsr.Station(5613206)
        self.assertEqual(x._latitude, None)
        self.assertEqual(x._longitude, None)
        c = x.coordinates()
        self.assertNotEqual(x._latitude, None)
        self.assertNotEqual(x._longitude, None)
    def test_uic(self):
        x = zsr.Station(5613206)
        self.assertEqual(x.uic(), "5613206")
    def test_uic2(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x = zsr.Station("hello")
            self.assertEqual(x.name(), None)
    def test_key(self):
        x = zsr.Station("5613206")
        self.assertEqual(x.key(), "BRATISLAVA HL.ST.")
            

        
if __name__ == '__main__':
    unittest.main()