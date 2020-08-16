
# global imports
import logging
from urllib.error import HTTPError,URLError
# local imports
from . import common

# logging
logger = logging.getLogger(__name__)

def departures(uicCode, dt=None, departure=True):
    """Lists departures or arrivals from station.
    
    The station is given by *uicCode*, number in string format, text for big stations (e.g. "BRATISLAVA").
    The list contains items arriving/departing earliest at datetime *dt*.
    
    Args:
        uicCode (str): identifier of station, number or text.
        dt (datetime, optional): initial datetime of list, defaultly now()
        departure (bool, optional): list departures (True) or arrivals (False), defaultly True
    Returns:
        list: list of departing/arriving trains
    """
    # parse parameters
    if not uicCode: return {}
    station_prefix = common._urlencode(uicCode)
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

__all__ = ["departures"]