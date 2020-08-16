

# global imports
import logging
from urllib.error import HTTPError,URLError
import warnings
# local imports
from . import cache
from . import common

# logging
logger = logging.getLogger(__name__)

def search_stations(prefix, limit=10):
    """Queries for stations matching given prefix.
    
    Args:
        prefix (str): String prefix to query stations.
                              Case- and diacritic- insensitive.
        limit (str, optional): List limit. Default is 10.
    Returns:
        list: list of matched stations
    """
    if not prefix: return {}
    prefix = common._urlencode(prefix)
    # send request
    try:
        response = common._get_slovakrail( 
            path = f'/api/v1/station/name/{prefix}', 
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

def station(uicCode):
    """Maps uicCode to station name.
    
    Args:
        uicCode (str): Code of station.
    Returns:
        dict: station data
    """
    try:
        station_name = cache.lookup(uicCode)
        for s in search_stations(station_name):
            if s['uicCode'] == str(uicCode):
                return s
    except: pass
    raise KeyError('no station with given uicCode found')

__all__ = ["search_stations","station"]   