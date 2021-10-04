
# global imports
from datetime import datetime,date,time,timedelta
# local imports
from . import departures
from . import routes
from . import station

# logging
import logging
logger = logging.getLogger(__name__)

def _dep_id(station, arrival=False):
    dt_key = 'arrivalTimestamp' if arrival else 'departureTimestamp'
    return f"{station['trainStation']['uicCode']}{station[dt_key]}"

def get_daily_lines(dt=None):
    end = False
    # stop departures
    stop_departures = departures.daily_departures(dt=dt)
    linked_departures = {}
    for start,start_deps in stop_departures.items():
        for dep in start_deps:
            print(start, dep['to'], dep['dt'])
            rts = routes.search_routes(
                start=start,
                end=dep['to'],
                dt=datetime.strptime(dep['dt'],'%Y-%m-%d %H:%M:%S')
            )
            stops = rts[0]['routeSegments'][0]['trainStops']
            # create departure ids
            stops_id = [_dep_id(s) for s in stops[:-1]]
            stops_id.append(_dep_id(stops[-1], arrival=True))
            # go through links
            prev_link = None
            for i in range(len(stops_id),0,-1):
                stop_id = stops_id[i]
                # create new link
                if stop_id not in linked_departures:
                    linked_departures[stop_id] = prev_link
                # go to previous station
                else:
                    prev_link = stop_id
            print(rts[0])
            break
            #if stationA['arrivalTimestamp'] is None:
            #    print(
            #        stationA['arrivalTimestamp'],
            #        stationA['departureTimestamp'],
            #        stationA['trainStation']['uicCode'],
            #        stationA['trainStation']['name'],
            #        "-",
            #        stationB['arrivalTimestamp'],
            #        stationB['departureTimestamp'],
            #        stationB['trainStation']['uicCode'],
            #        stationB['trainStation']['name'])
            #    end = True
            #    break
            #break
        #if end:
        #    break
        break

__all__ = ['get_daily_lines']