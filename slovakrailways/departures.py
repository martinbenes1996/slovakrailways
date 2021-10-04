
# global imports
from datetime import datetime,date,time,timedelta
import pandas as pd
# local imports
from . import _common
from . import station

# logging
import logging
logger = logging.getLogger(__name__)

def search_departures(stationA, dt=None, departure=True):
    """Lists departures or arrivals from station.
    
    The station is given as a pandas station, number in string format.
    The list contains items arriving/departing earliest at datetime *dt*.
    
    Args:
        stationA (dict): Station data frame.
        dt (datetime, optional): initial datetime, defaultly now().
        departure (bool, optional): list departures (True) or arrivals (False), defaultly True
    Returns:
        list: list of departing/arriving trains
    """
    # parse parameters
    travelDate = _common._parse_date(dt) # UNIX timestamp [ms]
    departure = int(departure)
    uicCode = stationA.reset_index(drop=True).loc[0,"uicCode"]
    # send request
    response = _common.get_slovakrail(
        path = f'/api/v2/station/{uicCode}/roster', 
        parameters = {
            'departure': departure,
            'travelDate': travelDate
        }
    )
    # parse departures
    departures = []
    for dep in response:
        # departure
        depIsDep = dep['isDeparture']
        depStation = dep['station']
        depTimestamp = _common._parse_timestamp(dep['timestamp'])
        depTrainType = dep['train']['type']
        depTrainName = dep['train']['name']
        depTrainTypeList = dep['train']['typeList']
        depTrainNumber = dep['train']['number']
        depTrainCarrier = dep['train']['carrier']
        depTrainDelay = dep['train']['trainDelay']
        # map stations
        depStationA = station.of_uic(uicCode)\
            .reset_index(drop=True)
        try:
            depStationB = station.of_key(depStation,is_domestic=False)\
                .reset_index(drop=True)
        except:
            logger.error(f"error getting uic of station \"{depStation}\"")
            continue
        # save
        departure = {
            'A': uicCode,
            'B': depStationB.loc[0,'uicCode'],
            'dt': depTimestamp,
            'trainType': depTrainType,
            'trainName': depTrainName,
            'trainNumber': depTrainNumber,
            'trainCarrier': depTrainCarrier
        }
        departures.append(departure)
    # 
    return departures

def daily_departures(dt=None):
    """"""
    # cached
    import json
    with open('output.json') as fp:
        stop_departures = json.load(fp)
    return stop_departures
    if dt is None:
        dt = datetime.combine(datetime.now().date(), time.min)
    dtmax = datetime.combine(dt.date(), time.min) + timedelta(hours=8)#time.max)
    #print("Date:", dt, "Max:", dtmax)
    stop_departures = {}
    # iterate stations
    for s in station.iterate_stations():
        # set date to midnight (given date)
        dttime = datetime.combine(dt.date(), time.min)
        # fetch departures of station at dttime
        logger.info(f"fetching departures from {s.loc[0,'name']} [{s.loc[0,'uicCode']}]")
        departures = search_departures(s, dttime)
        # filter departures
        departures = [dep for dep in departures if dep['dt'] < dtmax]
        logger.info(f"acquired {len(departures)} departures")
        # append to departures
        for dep in departures:
            if dep['A'] not in stop_departures:
                stop_departures[dep['A']] = []
            stop_departures[dep['A']].append({
                'to': dep['B'],
                'dt': dep['dt'].strftime('%Y-%m-%d %H:%M:%S')
            })

    # output
    import json
    with open('output.json', 'w') as fp:
        json.dump(stop_departures, fp)
    return stop_departures

__all__ = ['search_departures','daily_departures']