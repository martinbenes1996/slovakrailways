# -*- coding: utf-8 -*-
"""Slovak Railways API.

This module contains functions to call Slovak Railways API.
For more information check README.md.
 
Reference: https://github.com/martinbenes1996/slovakrailways
Todo:
    * delays of multiple trains at single request
    * caching
"""

from .station import *
from .departure import *
from .train import *
from .route import *

from . import meta

# logging
import logging
logger = logging.getLogger(__name__)

# https://github.com/Zippersk/API-slovak-rail

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logger.warning("slovakrailways module not executable")