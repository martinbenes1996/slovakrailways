
import datetime
import logging
import sys
sys.path.append('.')

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

import __init__ as slovakrailways

# information of Zilina stations
def station_information():
    zilina_stations = slovakrailways.stations('Zilina')
    for station in zilina_stations:
        print(station)

# stations by prefix
def stations_by_prefix():
    rimavsk_stations = slovakrailways.stations('rimavsk')
    for station in rimavsk_stations:
        print(station)

# departures from station
def departures_from_station():
    # get Rimavska Sobota id
    station_id = slovakrailways.stations('rimavska sobota')[0]['uicCode']
    # get trains departing later today (3 h from now)
    dt = datetime.datetime.now() + datetime.timedelta(hours = 3)
    rimavska_sobota_departures = slovakrailways.departures(station_id, dt)
    for departure in rimavska_sobota_departures:
        print(departure)
        
# delay of train
def train_delay():
    # trains between Bratislava and Kosice
    dt = datetime.datetime.now() - datetime.timedelta(hours = 4)
    rt = slovakrailways.route(start='5613206',end='5613600', dt=dt)
    print(f"received {len(rt)} routes")
    # first result, first segment train
    train_number = rt[0]['routeSegments'][0]['train']['number']
    p = slovakrailways.delay(train_number)
    print(p)

# route between two stations
def routes_between():
    routes = slovakrailways.route('5613206','5613600')
    for r in routes:
        print(r)
        
# pricing from route
def pricing_from_route():
    # get trains going from Bratislava to Kosice
    rt = slovakrailways.route('5613206','5613600')
    print(f"received {len(rt)} routes")
    p = slovakrailways.pricing(rt[0]['routeSelfRefs'])
    #p = slovakrailways.pricing([369,-1678484520,134,3,88015,525931,525572])
    print(p)
    
pricing_from_route()

#print(slovakrailways.meta.age_categories())
