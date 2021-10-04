# -*- coding: utf-8 -*-
"""Slovak Railways API.

This module contains functions to call Slovak Railways API.
 
Todo:
    * delays of multiple trains at single request
    * caching
"""

# global imports
from urllib.error import HTTPError,URLError
# local imports
from . import _common
from . import meta

# logging
import logging
logger = logging.getLogger(__name__)
    
def search_routes(start, end, dt=None, departure=True, age_category=103, discount=1):
    """Lists connections for route between two points.
    
    Lists connections between start and end, given by uicCode's.
    The connections depart from start earliest at datetime dt.
    You can specify age category and discounts, for available ones call *slovakrailways.meta.age_categories()*.
    
    Args:
        start (str): uicCode of start station
        end (str): uicCode of end station
        dt (str, optional): time of departure/arrival, default is now()
        age_category (int, optional): age category of passenger
        discount (int,optional): age category discount
    Returns:
        list: connections between the start and end point
    """
    # parse parameters
    if not start or not end: return {}
    dt = _common._parse_date(dt) # UNIX timestamp [ms]
    # send request
    parameters = {'fromStation': start, 'toStation': end, # route endpoints
                  'travelDate': dt, # travel date
                  'departure': '1' if departure else '0'}#, # inverted if false (arrival)
                  #'ageCategory': age_category, 'ageCategoryDiscount': discount} # pricing
    response = _common.get_slovakrail(
        path = f'/api/v2/route/',
        parameters = parameters)
    # result
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
    dt = _common._parse_date(dt) # UNIX timestamp [ms]
    route_ref_query = _common._multiname_urlparam('selfRef', route_ref) # route_ref to multiname url parameters
    # contruct request
    parameters = {
        'travelDate': dt, # travel date
        'order': 1 if order else 0, # ???
        'ageCategory': age_category,
        'ageCategoryDiscount': discount, # pricing
        'freeTransportDiscount': 'true' if free else 'false'} # free of charge
    # send request
    response = _common.get_slovakrail(
        path = f'/api/v1/route/pricing',
        parameters = parameters,
        paramstring = route_ref_query)
    # OK
    return response

__all__ = ["search_routes","pricing"]