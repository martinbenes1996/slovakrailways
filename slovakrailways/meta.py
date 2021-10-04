
# local imports
from . import _cache
from . import _common
from . import _meta
from . import cache

# logging
import logging
logger = logging.getLogger(__name__)

class TrainType:
    @classmethod
    def to_value(cls, name, use_cache=True):
        """Maps train type name onto value.
        
        Args:
            name (str): Train type name.
            use_cache (bool): Use cache, True by default.
        Returns:
            (int): Train type value (for mask).
        """
        # read from cache
        try:
            if not use_cache: raise Exception
            train_type_cache = _cache.TrainTypes.get()
            value = train_type_cache.to_value(name=name)
            logger.debug("getting cached train types")
        # fetch and read
        except:
            logger.debug("fetching train types")
            train_types = _meta.fetch_train_types()
            value = train_types[train_types.name == name]['value']
            value = value.reset_index(drop=True)[0]
        return value
    
    @classmethod
    def to_description(cls, name, use_cache=True):
        """Maps train type name onto description.
        
        Args:
            name (str): Train type name.
            use_cache (bool): Use cache, True by default.
        Returns:
            (int): Train type description.
        """
        # read from cache
        try:
            if not use_cache: raise Exception
            train_type_cache = _cache.TrainTypes.get()
            description = train_type_cache.to_description(name=name)
            logger.debug("getting cached train types")
            return description
        # fetch and read
        except:
            logger.debug("fetching train types")
            train_types = _meta.fetch_train_types()
            return train_types[train_types.name == name]['description']\
                .reset_index(drop=True)[0]
    
    @classmethod
    def mask(cls, trainTypes):
        value = 0
        for ttype in trainTypes:
            value = value | cls.to_value(ttype)
        return value

def api_status():
    """Check status of ZSR API, True or False."""
    # test api version (and connect)
    try:
        return _common.get_slovakrail('/api/supported-version/2')
    # catch error
    except:
        return False