
import urllib.parse
import urllib.request
import datetime
import json

# logging
import logging
logger = logging.getLogger(__name__)

api_key_hdr = {'x-api-key': 'PDh^2-$-M]8(dG8E+Q,FR}zsfz"Q~:N2pp\ykmg9ZEgKVrh42PHS?^sQ6<3;X,?-'}
slovakrail_url = 'https://app.slovakrail.sk'

def _get_slovakrail(path, parameters={}, headers={}, data=None, paramstring=""):
    # construct url
    url = slovakrail_url + path
    # add parameters
    paramstring += "&" if paramstring else ""
    if parameters:
        url += "?" + paramstring + urllib.parse.urlencode(parameters)
    # add api key to headers
    headers = {**api_key_hdr, **headers}
    # data
    if data is not None:
        headers['Content-Type'] = 'application/json; charset=utf-8'
        data = bytes(json.dumps(data), encoding="utf-8")
    # send request
    logger.debug(f"GET {url}")
    if data is not None: logger.debug(data)
    req = urllib.request.Request(url, data=data, headers=headers)
    response = urllib.request.urlopen(req) # raises HTTPError if error
    logger.debug(f"response status {response.getcode()}")
    # process response
    response_data = json.loads(response.read().decode('utf-8'))
    return response_data

def _parse_date(dt):
    if dt is None:
        dt = datetime.datetime.today() # now
    # datetime -> UNIX timestamp
    dt = int(datetime.datetime.timestamp(dt))
    dt *= 1000 # ms
    return dt
def _urlencode(s): return urllib.parse.quote_plus(str(s))
def _multiname_urlparam(key, values):
    key = urllib.parse.quote_plus(key)
    q = ""
    for i,v in enumerate(values):
        q += key + "=" + urllib.parse.quote_plus(str(v)) + "&"
    return q[:-1] # remove last "&"

__all__ = ["_get_slovakrail","_parse_date","_urlencode","_multiname_urlparam"]