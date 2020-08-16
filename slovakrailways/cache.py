
import csv
import pkg_resources

class Cache:
    _cache_location = pkg_resources.resource_filename(__name__, "data/uic.csv")
    _cache_data = None
    _cache = None
    def __init__(self):
        with open(self._cache_location, encoding = "utf-8") as fd:
            data = csv.reader(fd)
            self._cache_data = {uic:name for uic,name in data}
    def __getitem__(self, key):
        return self._cache_data[key]
    @classmethod
    def get(cls):
        if not cls._cache:
            cls._cache = cls()
        return cls._cache
    @classmethod
    def lookup(cls, uic):
        return cls.get()[str(uic)]
    
def lookup(uic):
    return Cache.lookup(uic)

__all__ = ["lookup"]
                    
            