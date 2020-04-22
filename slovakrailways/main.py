# -*- coding: utf-8 -*-
"""Slovak Railways API.

This module contains functions to call Slovak Railways API.
 
Todo:
    * delays of multiple trains at single request
    * caching
"""

# global imports
import datetime
import json
import logging
from urllib.error import HTTPError,URLError
# local imports
import common

# logging
logger = logging.getLogger(__name__)

def stations(station_prefix, limit=10):
    """Queries for stations matching given prefix.
    
    Args:
        station_prefix (str): String prefix to query stations.
                              Case- and diacritic- insensitive.
        limit (str, optional): List limit. Default is 10.
    Returns:
        list: list of matched stations
    """
    if not station_prefix: return {}
    station_prefix = common._urlencode(station_prefix)
    # send request
    try:
        response = common._get_slovakrail( 
            path = f'/api/v1/station/name/{station_prefix}', 
            parameters = {'maxCount': limit})
        
    # error
    except (HTTPError,URLError) as e: 
        try: msg = e.msg if e.msg else "<no message>"
        except: msg = "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return {}
    # OK
    return response

def departures(station_id, dt=None, departure=True):
    """Lists departures or arrivals from station.
    
    The station is given by *station_id*, number in string format, text for big stations (e.g. "BRATISLAVA").
    The list contains items arriving/departing earliest at datetime *dt*.
    
    Args:
        station_id (str): identifier of station, number or text.
        dt (datetime, optional): initial datetime of list, defaultly now()
        departure (bool, optional): list departures (True) or arrivals (False), defaultly True
    Returns:
        list: list of departing/arriving trains
    """
    # parse parameters
    if not station_id: return {}
    station_prefix = common._urlencode(station_id)
    dt = common._parse_date(dt) # UNIX timestamp [ms]
    departure = 'true' if departure else 'false'
    
    # send request
    try:
        response = common._get_slovakrail(
            path = f'/api/v1/station/{station_prefix}/roster', 
            parameters = {'departure': departure, 'travelDate': dt})
    # error
    except (HTTPError,URLError) as e:
        try: msg = e.msg if e.msg else "<no message>"
        except: msg = "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return {}
    # OK
    return response
    
def delay(train_number, dt=None):
    """Returns current position and delay of a particular train.
    
    Train is identified by *train_number*.
    The state is for datetime dt, leave None for now().
    
    Args:
        train_number (str): number of train to get status of
        dt (datetime, optional): datetime of state
    Returns:
        dict: description of the status
    """
    # parse parameters
    if not train_number: return {}
    dt = common._parse_date(dt) # UNIX timestamp [ms]
    
    # send request
    try:
        response = common._get_slovakrail(
            path = f'/api/v1/train/delay', 
            data = [{'trainNumber': train_number, 'travelDate': dt}])
    
    # error
    except (HTTPError,URLError) as e: 
        try: msg = e.msg if e.msg else "<no message>"
        except: msg = "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return {}
    # OK
    return response[0]

def route(start, end, dt=None, departure=True, age_category=103, discount=1):
    """Lists connections for route between two points.
    
    Lists connections between start and end, given by station_ids.
    The connections depart from start earliest at datetime dt.
    You can specify age category and discounts, for available ones call *slovakrailways.meta.age_categories()*.
    
    Args:
        start (str): station_id of start station
        end (str): station_id of end station
        dt (str, optional): time of departure/arrival, default is now()
        age_category (int, optional): age category of passenger
        discount (int,optional): age category discount
    Returns:
        list: connections between the start and end point
    """
    # parse parameters
    if not start or not end: return {}
    dt = common._parse_date(dt) # UNIX timestamp [ms]
    
    # send request
    parameters = {'fromStation': start, 'toStation': end, # route endpoints
                  'travelDate': dt, # travel date
                  'departure': 'true' if departure else 'false', # inverted if false (arrival)
                  'ageCategory': age_category, 'ageCategoryDiscount': discount} # pricing
    try:
        response = common._get_slovakrail(
            path = f'/api/v1/route/',
            parameters = parameters)
    
    # error
    except (HTTPError,URLError) as e:
        try: msg = e.msg if e.msg else "<no message>"
        except: msg = "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return {}
    # OK
    else: 
        return response
    
def pricing(route_reference, dt=None, age_category=103, discount=1, free=False, order=False):
    """Gets pricings for given route.
    
    Gets route reference, a list of specific numbers.
    Computes the price given *age_category* and *discount* (or free of charge - students).
    
    Args:
        route_reference (list):
        dt (datetime, optional):
        age_category (int, optional):
        discount (int, optional):
        free (bool, optional):
        order (bool, optional):
    Returns:
        dict: options of travel (keys 'segmentOptions','optionPricings')
    """   
    # process parameters
    if not route_reference or len(route_reference) != 7: return {}
    route_ref = []
    for it in route_reference:
        try:
            route_ref.append(int(it))
        except:
            route_ref.append(int(it['selfRef']))
    dt = common._parse_date(dt) # UNIX timestamp [ms]
    route_ref_query = common._multiname_urlparam('selfRef', route_ref) # route_ref to multiname url parameters
    
    # send request
    parameters = {'travelDate': dt, # travel date
                  'order': 1 if order else 0, # ???
                  'ageCategory': age_category, 'ageCategoryDiscount': discount, # pricing
                  'freeTransportDiscount': 'true' if free else 'false'} # free of charge
    try:
        response = common._get_slovakrail(
            path = f'/api/v1/route/pricing',
            parameters = parameters,
            paramstring = route_ref_query)
        
    # error
    except (HTTPError,URLError) as e:
        try: msg = e.msg if e.msg else "<no message>"
        except: msg = "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return []
    # OK
    else:
        return response

# https://github.com/Zippersk/API-slovak-rail

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger.warning("slovakrailways module not executable")
else:
    logger.debug("slovakrailways loaded")

__all__ = ["stations","departures","delay","route","pricing"]