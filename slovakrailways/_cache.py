# global imports
import pandas as pd
import pkg_resources
import sqlite3
# local imports
from . import _meta

# logging
import logging
logger = logging.getLogger(__name__)

class Cache:
    @classmethod
    def _get_instance(cls):
        """Abstract singleton instance getter.
        
        Returns:
            (child of Cache): Singleton instance.
        """
        raise NotImplementedError
    @classmethod
    def _set_instance(cls, instance):
        """Abstract singleton instance setter.
        
        Args:
            instance (child of Cache): Singleton instance.
        """
        raise NotImplementedError
    @classmethod
    def get(cls):
        """Get cache singleton instance."""
        if not cls._get_instance():
            cls._set_instance(cls())
        return cls._cache
    def __init__(self, location, table):
        """Constructor.
        
        Args:
            location (str): Name of cache file.
            table (str): Table name.
        """
        self._table = table
        self._cache_location = pkg_resources.resource_filename(__name__, f"data/{location}")
        try:
            conn = sqlite3.connect(self._cache_location)
            self._cache_data = pd.read_sql(f'SELECT * FROM {table}', conn)
            #self._cache_data = pd.read_csv(self._cache_location)
        except:
            logger.error("empty cache, need to fetch")
            self._cache_data = None
    def __getitem__(self, item):
        """Abstract item getter."""
        raise NotImplementedError
    def write(self, cache_data):
        """Write data to sqlite.
        
        Args:
            cache_data (pd.DataFrame): Data to cache.
        """
        conn = sqlite3.connect(self._cache_location)
        self._cache_data = cache_data
        try:
            self._cache_data.to_sql(self._table, conn, index=False)
        except:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE {self._table}")
            self._cache_data.to_sql(self._table, conn, index=False)
        conn.commit()
        conn.close()
    def data(self):
        """Abstract getter of cache content."""
        raise NotImplementedError

class Station(Cache):
    _cache = None
    @classmethod
    def _get_instance(cls):
        return cls._cache
    @classmethod
    def _set_instance(cls, instance):
        cls._cache = instance
    def __init__(self):
        super().__init__('cache.sqlite','stations')
        logger.info("creating Stations cache")
        if self._cache_data is not None:
            self._cache_data['domestic'] = self._cache_data.domestic.apply(bool)
    def __getitem__(self, item):
        return self.of_uic(uicCode=item)
    def of_key(self, subname):
        subkey = _meta.to_key(subname)
        return self._cache_data[self._cache_data.key.str.contains(subkey, case=False, regex=False)]
    def of_uic(self, uicCode):
        return self._cache_data[self._cache_data.uicCode == uicCode]
    def data(self):
        return self._cache_data

class TrainTypes(Cache):
    _cache = None
    @classmethod
    def _get_instance(cls):
        return cls._cache
    @classmethod
    def _set_instance(cls, instance):
        cls._cache = instance
    def __init__(self):
        super().__init__('cache.sqlite','traintypes')
        logger.info("creating TrainTypes cache")
    def __getitem__(self, item):
        return self.of_uic(uicCode=item)
    def to_value(self, name):
        value = self._cache_data[self._cache_data.name == name]['value']
        return value.reset_index(drop=True)[0]
    def to_description(self, name):
        description = self._cache_data[self._cache_data.name == name]['description']
        return description.reset_index(drop=True)[0]
    def data(self):
        return self._cache_data

class Departure(Cache):
    _cache = None
    @classmethod
    def _get_instance(cls):
        return cls._cache
    @classmethod
    def _set_instance(cls, instance):
        cls._cache = instance
    def __init__(self):
        super().__init__('cache.sqlite','departures')
        logger.info("creating Departures cache")
    def data(self):
        return self._cache_data

__all__ = ["Station"]