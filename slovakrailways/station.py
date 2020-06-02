
from . import cache
from . import main
from . import meta
from . import connection
from .connection import Connection

class Station:
    _cache = None
    @classmethod
    def uic_to_name(cls, uic):
        if cls._cache is None:
            cls._cache = cache.cache_uic()
        try:
            return cls._cache[uic]
        except:
            return None
    @classmethod
    def get(cls, prefix, exact = False):
        stations = main.stations(prefix)
        stationList = []
        if exact:
            for s in stations:
                if prefix == s['name']:
                    return cls(**s)
            else:
                return None
        for s in stations:
            try:
                uic = int(s['uicCode'])
            except:
                continue
            else:
                stationList.append( cls(**s) )
        return stationList
                
    def __init__(self, uicCode, **kwargs):
        self._uic = uicCode
        self._name = self.uic_to_name(self._uic)
        self._lazy = "lazy" not in kwargs or kwargs["lazy"]
        if self._lazy:
            if self._name is None:
                self._name = kwargs["name"] if "name" in kwargs else None
            self._latitude = kwargs["latitude"] if "latitude" in kwargs else None
            self._longitude = kwargs["longitude"] if "longitude" in kwargs else None
            self._departures = {}
        else:
            if "name" not in kwargs or "latitude" not in kwargs or "longitude" not in kwargs:
                self._fetch_stations()
            else:
                if self._name is None:
                    self._name = kwargs["name"]
                self._latitude = kwargs["latitude"]
                self._longitude = kwargs["longitude"]
    def uic(self):
        return self._uic
    def name(self):
        if self._name is None:
            self._fetch_station()
        return self._name
    def coordinates(self):
        if self._latitude is None or self._longitude is None:
            self._fetch_station()
        return (self._latitude, self._longitude)
    def departures(self):
        deps = Connection.departures(self)
        return deps
        #print(deps)
    def _fetch_station(self):
        prefix = self.uic_to_name(self._uic)
        stations = main.stations(prefix)
        for s in stations:
            if s['uicCode'] == self._uic:
                if self._name is None:
                    self._name = s['name']
                self._latitude = s['latitude']
                self._longitude = s['longitude']
                break
        
    def __repr__(self):
        name = f"\"{self._name}\"" if self._name is not None else "?"
        return f"<Station {name} [{self._uic}]>"
    def __eq__(self, other):
        return self._uic == other.uic()
        
# dependency injection
connection.Station = Station

__all__ = ["Station"]   