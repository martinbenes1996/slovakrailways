
# global imports
import logging
import sys
from urllib.error import HTTPError,URLError
# local imports
from . import common
from . import meta

# logging
logger = logging.getLogger(__name__)

def track_train(trainNumber, dt=None):
    """Returns current position and delay of a particular train.
    
    Train is identified by *trainNumber*.
    The state is for datetime dt, leave None for now().
    
    Args:
        trainNumber (str): number of train to get status of
        dt (datetime, optional): datetime of state
    Returns:
        dict: description of the status
    """
    # parse parameters
    if not trainNumber: return {}
    dt = common._parse_date(dt) # UNIX timestamp [ms]
    
    # send request
    try:
        response = common._get_slovakrail(
            path = f'/api/v1/train/delay', 
            data = [{'trainNumber': trainNumber, 'travelDate': dt}])
    
    # error
    except (HTTPError,URLError) as e: 
        try: msg = e.msg if e.msg else "<no message>"
        except: msg = "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return {}
    # OK
    return response

__all__ = ["track_train"]