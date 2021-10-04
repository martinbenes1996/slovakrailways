
# global imports
import pandas as pd
from scipy.stats import uniform
from string import ascii_lowercase
import time
# local imports
from . import _cache
from . import _common
from . import _meta

# logging
import logging
logger = logging.getLogger(__name__)

def fetch_stations_with_prefix(prefix, limit=10):
    """Queries for stations matching given prefix.
    
    Args:
        prefix (str): String prefix to query stations.
                              Case- and diacritic- insensitive.
        limit (str, optional): List limit. Default is 10.
    Returns:
        list: list of matched stations
    """
    if not prefix: return {}
    prefix = _common._urlencode(prefix)
    # send request
    response = _common.get_slovakrail( 
        path = f'/api/v2/station/name/{prefix}', 
        parameters = {'maxCount': limit})
    # to dataframe
    columns = ['uicCode','name','image','latitude','longitude']
    data = pd.DataFrame([s.values() for s in response], columns=columns)
    # create derivative columns
    data['domestic'] = (abs(data.latitude - .0) > .001)|(abs(data.longitude - .0) > 0.001)
    data['key'] = data.name.apply(_meta.to_key)
    # OK
    return data

def _sleep(delay):
    if delay is None: return
    try:
        time.sleep(float(delay))
    except: 
        delay = uniform.rvs(delay[0], sum(delay))
        time.sleep(delay)

def _fetch_prefix_recursive(prefix, total=0):
    # fetch data of prefix
    #print(prefix, end="")
    station_data = fetch_stations_with_prefix(prefix=prefix, limit=100)
    #print(f" {station_data.shape[0]}", end=" | ")
    # less than 90 records
    if station_data.shape[0] < 90:
        return station_data
    # add letter to prefix
    else:
        data,data_sum = None,0
        for letter in ascii_lowercase:
            prefix_data = _fetch_prefix_recursive(prefix + letter, total=station_data.shape[0])
            data_sum += prefix_data.shape[0]
            data = prefix_data if data is None else pd.concat([data, prefix_data])
        return data

def fetch_all_stations(delay1=None, delay2=None):
    columns = ['uicCode','name','image','latitude','longitude','key','domestic']
    data = pd.DataFrame([], columns=columns)
    # create two letter prefix
    for letter1 in ascii_lowercase:
        logger.info(f"fetching stations with prefix {letter1}-")
        for letter2 in ascii_lowercase:
            # fetch stations of the prefix
            prefix_data = _fetch_prefix_recursive(prefix=letter1 + letter2)
            data = prefix_data if data is None else pd.concat([data, prefix_data])
            # sleep
            _sleep(delay2)
        _sleep(delay1)
    return data

def of_key(subname, is_domestic=True, use_cache=True):
    """Maps a station name substring to the station data.
    
    Args:
        subname (str): Substring of the station name or prefix (if not in cache).
        is_domestic (bool): Show only domestic, True by default.
        use_cache (bool): Use cache, True by default.
    Returns:
        (pd.DataFrame): matched stations
    """
    # get from cache
    try:
        if not use_cache: raise Exception
        station_cache = _cache.Station.get()
        station_data = station_cache.of_key(subname=subname)
        logger.debug("getting cached prefix stations")
    # fetch
    except Exception as e:
        logger.debug("fetching prefix stations")
        station_data = fetch_stations_with_prefix(prefix=subname, limit=100)
    # domestic
    if is_domestic:
        station_data = station_data[station_data.domestic]
    # no station found
    if station_data.empty:
        raise KeyError(f'no station with given key {subname} found')
    # return
    return station_data\
        .reset_index(drop=True)

def of_uic(uicCode, use_cache=True):
    """Gets a station.
    
    Args:
        uicCode (str): UIC code of station.
        use_cache (bool): Use cached data. True by default.
    Returns:
        (pd.DataFrame): found station
    """
    # get from cache
    try:
        if not use_cache: raise Exception
        logger.debug("getting cached uic stations")
        station_cache = _cache.Station.get()
        station_data = station_cache.of_uic(uicCode=uicCode)
    # fetch
    except Exception as e:
        raise KeyError("can't get a station without cache")
    # no station found
    if station_data.empty:
        raise KeyError('no station with given key found')
    # return
    return station_data\
        .reset_index(drop=True)

def iterate_stations(is_domestic=True, use_cache=True):
    """Iterate stations.

    Args:
        is_domestic (bool): Yield only domestic, True by default.
        use_cache (bool): Use cache, True by default.
    Returns:
        (generator of str): uicCodes of stations
    """
    # get from cache
    try:
        if not use_cache: raise Exception
        logger.debug("getting cached data")
        station_cache = _cache.Station.get()
        station_data = station_cache.data()
    # fetch
    except Exception as e:
        raise KeyError("can't iterate stations without cache")
    # domestic
    if is_domestic:
        station_data = station_data[station_data.domestic]
    station_data = station_data.reset_index(drop=True)
    # row by row
    for i in range(station_data.shape[0]):
        yield station_data[station_data.index == i]\
            .reset_index(drop=True)
    #for row in station_data.itertuples():
    #    yield str(row.uicCode)

__all__ = ["fetch_stations_with_prefix","fetch_all_stations","of_uic","of_key","iterate_stations"]   