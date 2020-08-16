
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

class TestRoute(unittest.TestCase):
    def setUp(self):
        pass
        
    @delay_test(timeout = 1)
    def test_route(self):
        x = zsr.route("609")
        print(x)
        
    @delay_test(timeout = 1)
    def test_pricing(self):
        x = zsr.pricing("609")
        print(x)
        
        

__all__ = ["TestRoute"]