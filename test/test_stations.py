
import re
import sys
import unittest

sys.path.append(".")

import slovakrailways as zsr

class TestStations(unittest.TestCase):
    def setUp(self):
        self.f = zsr.stations
    
    def _query_station_regex_keys(self, stations):
        
        for station in stations:
            station = zsr.meta.to_key(station)
            yield f"^.*{station}.*$"
        
        
    def test_bratislava(self):
        x = self.f("bratislava")
        print(x)
        query_stations = [ zsr.meta.to_key(i["name"]) for i in x]
        
        bratislava_stations = ["bratislava hl.st.", "predmestie", "uns", "lamac",
                               "nove mesto","petrzalka", "raca", "vajnory", "vinohrady"]
        
        for station_regex in self._query_station_regex_keys(bratislava_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    
    def test_kosice(self):
        x = self.f("kosice")
        query_stations = [ zsr.meta.to_key(i["name"]) for i in x]
        
        for station_regex in self._query_station_regex_keys(["kosice", "predmestie"]):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    
    def test_presov(self):
        x = self.f("presov")
        query_stations = [ zsr.meta.to_key(i["name"]) for i in x]
        
        presov_stations = ["presov","mesto","as mhd","nemocnica j.a.reimana","pri mestskom cintorine","nizna sebastova"]
        for station_regex in self._query_station_regex_keys(presov_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)

    def test_zilina(self):
        x = self.f("zilina")
        query_stations = [ zsr.meta.to_key(i["name"]) for i in x]
        
        zilina_stations = ["zilina","solinky","zariecie"]
        for station_regex in self._query_station_regex_keys(zilina_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)

if __name__ == '__main__':
    unittest.main()