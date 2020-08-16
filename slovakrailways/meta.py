
from urllib.error import HTTPError,URLError

from . import common

# logging
import logging
logger = logging.getLogger(__name__)

_decoder = {
    "Á": "A", "á": "a", "Ä": "A", "ä": "a",
    "Č": "C", "č": "c",
    "Ď": "D", "ď": "d",
    "É": "E", "é": "e", "Ě":"E", "ě": "e", "Ä": "A", "ä": "a",
    "Í": "I", "í": "i", "Ï": "I", "ï": "i",
    "Ĺ": "L", "ĺ": "l", "Ľ": "L", "ľ": "l",
    "Ň": "N", "ň": "n",
    "Ó": "O", "ó": "o", "Ô": "O", "ô": "o", "Ö": "O", "ö": "o",
    "Ř": "R", "ř": "r", "Ŕ": "R", "ŕ": "r",
    "Š": "S", "š": "s",
    "Ť": "T", "ť": "t",
    "Ú": "U", "ú": "u", "Ü": "U", "ü": "u",
    "Ý": "Y", "ý": "y", "Ÿ": "Y", "ÿ": "y",
    "Ž": "Z", "ž": "z"
}
def to_key(s):
    letters = [letter for letter in s]
    result = ""
    for letter in letters:
        try:
            result += _decoder[letter].upper()
        except:
            result += letter.upper()
    return result



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

_description = None
def description():
    global _description
    if _description: return _description
    try:
        response = common._get_slovakrail('/api/v1/init')
    except (HTTPError,URLError) as e: # error
        msg = e.msg if e.msg else "<no message>"
        logger.error(f'Error {e.getcode()}: {msg}')
        logger.debug(e.info())
        return {}
    else:
        _description = response
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

__all__ = ["to_key", "status","description","age_categories","train_types","place_attributes"]