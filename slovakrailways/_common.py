
# global imports
from urllib import error,parse,request
from datetime import timedelta,datetime
import json

# logging
import logging
logger = logging.getLogger(__name__)

api_key_hdr = {'x-api-key': 'PDh^2-$-M]8(dG8E+Q,FR}zsfz"Q~:N2pp\ykmg9ZEgKVrh42PHS?^sQ6<3;X,?-'}
slovakrail_url = 'https://app.slovakrail.sk'

def _get_slovakrail(path, parameters={}, headers={}, data=None, paramstring=""):
    """Low-level HTTP GET call to ZSR API.
    
    Args:
        path ():
        parameters ():
        headers ():
        data ():
        paramstring ():
    Returns:
        (): Response data.
    """
    # construct url
    url = slovakrail_url + path
    # add parameters
    paramstring += "&" if paramstring else ""
    if parameters:
        url += "?" + paramstring + parse.urlencode(parameters)
    # add api key to headers
    headers = {**api_key_hdr, **headers}
    # data
    if data is not None:
        headers['Content-Type'] = 'application/json; charset=utf-8'
        data = bytes(json.dumps(data), encoding="utf-8")
    # send request
    logger.debug(f"GET {url}")
    #print(f"GET {url}")
    if data is not None: logger.debug(data)
    req = request.Request(url, data=data, headers=headers)
    response = request.urlopen(req) # raises HTTPError if error
    logger.debug(f"response status {response.getcode()}")
    # process response
    response_data = json.loads(response.read().decode('utf-8'))
    return response_data

def _try_call(f, default):
    try: return f()
    except: return default
def _try(f, messageF):
    try: f(messageF())
    except: pass
def get_slovakrail(*args, **kw):
    """"""
    # send request
    try:
        return _get_slovakrail(*args, **kw)
    # error
    except (error.HTTPError,error.URLError) as e:
        _try(logger.debug, lambda: e.info())
        _try(logger.debug, lambda: e.message())
        # acquire
        msg = _try_call(lambda: e.msg if e.msg else str(e), "<no message>")
        code = _try_call(lambda: e.getcode(), "<no code>")
        raise Exception(f'Error {code}: {msg}')

def _parse_date(dt = None):
    """Parse date.
    
    Args:
        dt ():
    """
    if dt is None:
        dt = datetime.today() # now
    # datetime -> UNIX timestamp
    dt = int(datetime.timestamp(dt))
    dt *= 1000 # ms
    return dt

def _parse_timestamp(dt = None):
    """Parse date.
    
    Args:
        dt ():
    """
    if dt is None:
        dt = datetime.now().timestamp() # now
    # UNIX timestamp -> datetime
    dt /= 1000 # s
    dt = datetime.fromtimestamp(dt)
    return dt

def _urlencode(s):
    """Backquotes s into URL format."""
    return parse.quote_plus(str(s))

def _multiname_urlparam(key, values):
    """Encodes the URL parameters into the URL format.
    
    Args:
        key ():
        values ():
    """
    key = parse.quote_plus(key)
    q = ""
    for i,v in enumerate(values):
        q += key + "=" + parse.quote_plus(str(v)) + "&"
    return q[:-1] # remove last "&"

def _construct_refs():
    search_dt = datetime(2020,6,30)
    departure_dt = datetime(2020,6,30)
    next_connection = 432307
    previous_connection = 432009
    ref1 = (search_dt - datetime(2020,6,29,14,15)) // timedelta(days = 49, hours = 17, minutes = 3) + 371
    ref3 = (departure_dt - datetime(2019,12,9)).days

__all__ = ["get_slovakrail","_parse_date","_urlencode","_multiname_urlparam"]