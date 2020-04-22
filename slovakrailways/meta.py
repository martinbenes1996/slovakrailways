
from urllib.error import HTTPError,URLError

import common

# logging
import logging
logger = logging.getLogger(__name__)

def status():
    try:
        response = common._get_slovakrail('/api/supported-version/1')
    except (HTTPError,URLError) as e: # error
        msg = e.msg if e.msg else "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return False
    else:
        return response
    
def description():
    try:
        response = common._get_slovakrail('/api/v1/init')
    except (HTTPError,URLError) as e: # error
        msg = e.msg if e.msg else "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return {}
    else:
        return response
def age_categories():
    response = description()
    # error
    if not response:
        return {}
    categories = response['ageCategories']
    return categories
def train_types():
    response = description()
    # error
    if not response:
        return {}
    types = response['trainTypes']
    return types
def place_attributes():
    response = description()
    # error
    if not response:
        return {}
    attributes = response['placeAttributes']
    return attributes

__all__ = ["status","description","age_categories","train_types","place_attributes"]