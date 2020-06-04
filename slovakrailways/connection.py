
from datetime import datetime

from . import _slovakrailways as zsr
from . import meta

# dependency injection design
Station = None

class Connection:
    station_cache = {}
    @classmethod
    def departures(cls, start = None, *args, **kwargs):
        if start is None:
            if "uic_code" not in kwargs and len(args) == 0:
                raise RuntimeError
            else:
                if "uic_code" in kwargs:
                    start = Station(kwargs["uic_code"])
                else:
                    start = Station(args[0])
        else:
            kwargs['uic_code'] = start.uic()
            
        deps = zsr.departures(*args, **kwargs)
        d = {}
        for dep in deps:
            if dep['station'] not in cls.station_cache:
                end = Station.get(dep['station'], exact = True)
                cls.station_cache[dep['station']] = end
            else:
                end = cls.station_cache[dep['station']]
            dt = datetime.utcfromtimestamp( int(dep['timestamp'])/1000 )
            d[dt] = cls(start, end, dt, dep)
        return d
    def __init__(self, start, end, dt = None, departure = None, route = None):
        self._start = start
        self._end = end
        self._dt = dt if dt is not None else datetime.now()
        
        self._train = [departure['train']] if departure is not None else None
        self._route = route
    
    def _parse_stops(self, segments):
        stops = []
        for segment in segments:
            for stop in segment['trainStops']:
                if not stop['trainStops']:
                    continue
                trainStop = {}
                try:
                    trainStop['arrival'] = datetime.utcfromtimestamp( int(stop['arrivalTimestamp'])/1000 )
                except:
                    trainStop['arrival'] = None
                try:
                    trainStop['departure'] = datetime.utcfromtimestamp( int(stop['departureTimestamp'])/1000 )
                except:
                    trainStop['departure'] = None
                trainStop['station'] = Station(**stop['trainStation'])
                stops.append(trainStop)
        return stops
    def _fetch_route(self):
        routes = zsr.route(self._start.uic(), self._end.uic(), self._dt)
        for rt in routes:
            # parse route stops
            rt_dt = datetime.utcfromtimestamp( int(rt['departureTimestamp'])/1000 )
            stops = self._parse_stops(rt['routeSegments'])
            
            # correct route?
            correct = 0
            for stop in stops:
                if correct == 0 and stop['station'] == self._start and stop['departure'] == rt_dt:
                    correct = 1
                if correct == 1 and stop['station'] == self._end:
                    correct = 2
                    break
            # no - continue
            if correct != 2:
                continue
            # yes
            #self._train = rt['train']
            self._route_ref = [m for m in map(lambda ref: ref['selfRef'], rt['routeSelfRefs'])]
            
            break
            
            
            
                    
        print(self._route_ref)
    def route(self):
        self._fetch_route()
    def __repr__(self):
        dt = self._dt.strftime("%Y-%m-%d %H:%M:%S")
        return f"<Connection {self._start.uic()} - {self._end.uic()} [{dt}]>"
        
        
        