# -*- coding: utf-8 -*-
"""Slovak Railways API.

This module contains functions to call Slovak Railways API.
For more information check README.md.
 
Reference: https://github.com/martinbenes1996/slovakrailways
Todo:
    * delays of multiple trains at single request
"""

from . import cache
from . import connections
#from . import departures
from . import meta
from . import station

from . import network

# logging
import logging
logger = logging.getLogger(__name__)

# https://github.com/Zippersk/API-slovak-rail

def search_station(prefix, is_domestic=True, use_cache=True):
    """Searches a station.

    Args:
        prefix (str): Prefix of station name to search. Substring for cached data.
        is_domestic (bool): Show only domestic stations. True by default.
        use_cache (bool): Use cached data. True by default.
    Returns:
        (pd.DataFrame): found match of stations
    """
    return station.of_key(subname=prefix, is_domestic=is_domestic, use_cache=use_cache)

def get_station(uicCode, use_cache=True):
    """Gets a station.
    
    Args:
        uicCode (str): UIC code of station.
        use_cache (bool): Use cached data. True by default.
    Returns:
        (pd.DataFrame): found station
    """
    try:
        return station.of_uic(uicCode=uicCode, use_cache=use_cache)
    except KeyError:
        logging.error("use cache_stations() prior to get_station() call")
        raise

def cache_stations():
    """Iterate over prefixes and cache all the acquired stations."""
    cache.cache_stations()

def cache_train_types():
    """Cache train types."""
    cache.cache_train_types()

def iterate_stations(is_domestic=True, use_cache=True):
    """Iterate stations.

    Args:
        is_domestic (bool): Yield only domestic, True by default.
        use_cache (bool): Use cache, True by default.
    Returns:
        (generator of str): uicCodes of stations
    """
    return station.iterate_stations(is_domestic=is_domestic, use_cache=use_cache)

def search_connections(fromUicCode, toUicCode, dt=None, departure=True,
                       changes={"viaUicCode": None, "direct": False, "max": 4, "minTime": 4, "maxTime": 180},
                       resources={"bed": 0, "bicycle": 0, "child": 0, "wheelChair": 0},
                       trainTypes=['Os','RR','R','IR','Ex','THALYS','EUROSTAR','EUROSTARITALIA','CISALPINO','AVE',
                                   'TALGO','rj','IC','SC','EC','ICE','TGV','EN','NZ','rjx','BUS','HST','Nez','ER',
                                   'CJX','REX','NJ','NT','NLT','EIC','ICB','TLK','EIP','RB','RE','Zr','Peší prechod']):
    """Lists departures or arrivals from station.
    
    The station is given by *uicCode*, number in string format, text for big stations (e.g. "BRATISLAVA").
    The list contains items arriving/departing earliest at datetime *dt*.
    
    Args:
        fromUicCode (str): Uic code of start station.
        toUicCode (str): Uic code of start station.
        dt (datetime, optional): initial datetime of list, defaultly now()
        departure (bool, optional): list departures (True) or arrivals (False), defaultly True
        changes (dict): Changes of connection. Options are whether the connection is direct (True or False),
                        maximal number of changes, minimal and maximal time for change (in minutes)
                        and Uic code of stop to go through. 
        resources (dict): Resources to allocate, i.e. bicycle, wheel chair, bed or baby carriage.
        trainTypes (list): Types of trains to use.
    Returns:
        list: list of departing/arriving trains
    """
    return connections.search_connections(
        fromUicCode=fromUicCode,
        toUicCode=toUicCode,
        dt=dt,
        departure=departure,
        changes=changes,
        resources=resources,
        trainTypes=trainTypes
    )

def api_status():
    """Check status of ZSR API, True or False."""
    return meta.api_status()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger.warning("slovakrailways module not executable")