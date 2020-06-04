import re
import sys
import unittest
import warnings

sys.path.append(".")

import slovakrailways._slovakrailways as zsr

class TestSlovakRailways(unittest.TestCase):
    def setUp(self):
        pass
    
    def _query_station_regex_keys(self, stations):
        for station in stations:
            station = zsr.meta.to_key(station)
            yield f"^.*{station}.*$"
            
    def test_stations_bratislava(self):
        x = zsr.stations("bratislava")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]

        bratislava_stations = ["bratislava hl.st.", "predmestie", "uns", "lamac",
                               "nove mesto","petrzalka", "raca", "vajnory", "vinohrady"]
        for station_regex in self._query_station_regex_keys(bratislava_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    def test_stations_kosice(self):
        x = zsr.stations("kosice")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]
        
        for station_regex in self._query_station_regex_keys(["kosice", "predmestie"]):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    
    def test_stations_presov(self):
        x = zsr.stations("presov")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]
        
        presov_stations = ["presov","mesto","as mhd","nemocnica j.a.reimana","pri mestskom cintorine","nizna sebastova"]
        for station_regex in self._query_station_regex_keys(presov_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)

    def test_stations_zilina(self):
        x = zsr.stations("zilina")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]
        
        zilina_stations = ["zilina","solinky","zariecie"]
        for station_regex in self._query_station_regex_keys(zilina_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    
    def test_stations_brno(self):
        x = zsr.stations("brno")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]
        
        brno_stations = ["dolni nadrazi","hl.n.","cernovice","chrlice","lesna",
                         "horni herspice","kralovo pole","reckovice","slatina"]
        for station_regex in self._query_station_regex_keys(brno_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            if not station_matched:
                print(station_regex)
            self.assertTrue(station_matched)