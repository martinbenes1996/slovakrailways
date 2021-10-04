# global imports
import pandas as pd
# local imports
from . import _common

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

_description = None
def description():
    global _description
    if _description: return _description
    _description = _common.get_slovakrail('/api/v2/init')
    return _description

def age_categories():
    response = description()
    # error
    if not response:
        return {}
    categories = response['ageCategories']
    return categories

def fetch_train_types():
    response = description()
    # error
    if not response:
        return {}
    train_types = response['trainTypes']
    # parse
    train_types = [(i['value'],i['name'],i['description']) for i in train_types]
    train_types = pd.DataFrame(train_types, columns = ['value','name','description'])
    return train_types

def place_attributes():
    response = description()
    # error
    if not response:
        return {}
    attributes = response['placeAttributes']
    return attributes

__all__ = ["to_key", "status","description","age_categories","train_types","place_attributes"]