
import re
import sys
import time
import unittest
import warnings

sys.path.append(".")

import slovakrailways as zsr

def delay_test(timeout = 1):
    def time_sleep_decorator(fn):
        def replace_time_sleep(*args, **kw):
            time.sleep(timeout)
            return fn(*args, **kw)
        return replace_time_sleep
    return time_sleep_decorator

class TestStation(unittest.TestCase):
    def setUp(self):
        pass
    
    def _query_station_regex_keys(self, stations):
        for station in stations:
            station = zsr.meta.to_key(station)
            yield f"^.*{station}.*$"
        
    @delay_test(timeout = 1)
    def test_list_bratislava(self):
        x = zsr.search_stations("bratislava")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x ]

        bratislava_stations = ["bratislava hl.st.", "predmestie", "uns", "lamac",
                               "nove mesto","petrzalka", "raca", "vajnory", "vinohrady"]
        for station_regex in self._query_station_regex_keys(bratislava_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    @delay_test(timeout = 1)
    def test_list_kosice(self):
        x = zsr.search_stations("kosice")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]
        
        for station_regex in self._query_station_regex_keys(["kosice", "predmestie"]):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    @delay_test(timeout = 1)
    def test_list_presov(self):
        x = zsr.search_stations("presov")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]
        
        presov_stations = ["presov","mesto","as mhd","nemocnica j.a.reimana","pri mestskom cintorine","nizna sebastova"]
        for station_regex in self._query_station_regex_keys(presov_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    @delay_test(timeout = 1)
    def test_list_zilina(self):
        x = zsr.search_stations("zilina")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]
        
        zilina_stations = ["zilina","solinky","zariecie"]
        for station_regex in self._query_station_regex_keys(zilina_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
    
    @delay_test(timeout = 1)   
    def test_stations_brno(self):
        x = zsr.search_stations("brno")
        query_stations = [ zsr.meta.to_key(i['name']) for i in x]
        
        brno_stations = ["dolni nadrazi","hl.n.","cernovice","chrlice","lesna",
                         "horni herspice","kralovo pole"] # reckovice,slatina missing for some reason
        for station_regex in self._query_station_regex_keys(brno_stations):
            # match station
            station_matched = any([bool(re.match(station_regex, qs)) for qs in query_stations])
            self.assertTrue(station_matched)
            
    @delay_test(timeout = 1)
    def test_error(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x = zsr.search_stations("hello")
            self.assertEqual(x, [])
    @delay_test(timeout = 1)
    def test_lookup_str(self):
        x = zsr.station("5613206")
        self.assertEqual(x['name'].upper(), "BRATISLAVA HL.ST.")
    @delay_test(timeout = 1)
    def test_lookup_int(self):
        x = zsr.station(5613206)
        self.assertEqual(x['name'].upper(), "BRATISLAVA HL.ST.")
    @delay_test(timeout = 1)
    def test_lookup_error(self):
        raised = False
        try: x = zsr.station(5)
        except: raised = True
        self.assertTrue(raised)
            
__all__ = ["TestStation"]