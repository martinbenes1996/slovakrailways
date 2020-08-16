
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

class TestDeparture(unittest.TestCase):
    def setUp(self):
        pass
    def _query_station_regex_keys(self, stations):
        for station in stations:
            station = zsr.meta.to_key(station)
            yield f"^.*{station}.*$"
        
    @delay_test(timeout = 1)
    def test_departures_bratislava(self):
        x = zsr.departures("5613206")
        self.assertIsInstance(x, list)
        for d in x:
            # departure
            self.assertIn('isDeparture', d)
            self.assertIsInstance(d['isDeparture'], bool)
            self.assertEqual(d['isDeparture'], True)
            # station
            self.assertIn('station', d)
            self.assertIsInstance(d['station'], str)
            # timestamp
            self.assertIn('timestamp', d)
            self.assertIsInstance(d['timestamp'], int)
            # train
            self.assertIn('train', d)
            self.assertIsInstance(d['train'], dict)
            # train type
            self.assertIn('type', d['train'])
            self.assertIsInstance(d['train']['type'], int)
            # train type list
            self.assertIn('typeList', d['train'])
            self.assertIsInstance(d['train']['typeList'], list)
            self.assertIn(d['train']['type'], d['train']['typeList'])
            # train number
            self.assertIn('number', d['train'])
            self.assertIsInstance(d['train']['number'], str)
            # train name
            self.assertIn('name', d['train'])
            self.assertIsInstance(d['train']['name'], str)
            # train features
            self.assertIn('features', d['train'])
            self.assertIsInstance(d['train']['features'], list)
            for f in d['train']['features']:
                self.assertIsInstance(f, dict)
                # train feature id
                self.assertIn('id', f)
                self.assertIsInstance(f['id'], int)
                # train feature description
                self.assertIn('featureDescription', f)
                self.assertTrue(not f['featureDescription'] or isinstance(f['featureDescription'], str))
                # train feature name
                self.assertIn('featureName', f)
                self.assertTrue(not f['featureDescription'] or isinstance(f['featureName'], str))
                # train feature order
                self.assertIn('order', f)
                self.assertIsInstance(f['order'], int)
                # train feature reservation type
                self.assertIn('reservationName', f)
                self.assertTrue(not f['reservationName'] or isinstance(f['reservationName'], str))
                # train feature indices
                self.assertIn('startStationIndex', f)
                self.assertIn('stopStationIndex', f)
            # train exceptions
            self.assertIn('exceptions', d['train'])
            self.assertIsInstance(d['train']['exceptions'], list)
            # train carrier
            self.assertIn('carrier', d['train'])
            self.assertIsInstance(d['train']['carrier'], str)
            # train delay
            self.assertIn('trainDelay', d['train'])
        
        

__all__ = ["TestDeparture"]