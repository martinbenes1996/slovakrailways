
# global imports
import pandas as pd
# local imports
from . import _cache
from . import _meta
from .station import fetch_all_stations

# logging
import logging
logger = logging.getLogger(__name__)

def cache_stations():
    # fetch stations
    stations = fetch_all_stations(delay1=(1,5), delay2=(0,.25))
    # write back
    stations_cache = _cache.Station.get()
    stations_cache.write(stations)

def cache_train_types():
    # fetch train types
    train_types = _meta.fetch_train_types()
    # write back
    train_types_cache = _cache.TrainTypes.get()
    train_types_cache.write(train_types)

if __name__ == "__main__":
    # config logging
    logging.basicConfig(level=logging.INFO)
    # cache stations
    cache_stations()
    # cache train types
    cache_train_types()
    # ...

__all__ = ["cache_stations"]