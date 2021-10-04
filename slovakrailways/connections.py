
# local imports
from . import _common
from . import meta

# logging
import logging
logger = logging.getLogger(__name__)

def search_connections(fromUicCode, toUicCode, dt=None, departure=True,
                       changes={"viaUicCode": None, "direct": False, "max": 4, "minTime": 4, "maxTime": 180},
                       resources={"bed": 0, "bicycle": 0, "child": 0, "wheelChair": 0},
                       trainTypes=['Os','RR','R','IR','Ex','THALYS','EUROSTAR','EUROSTARITALIA','CISALPINO','AVE',
                                   'TALGO','rj','IC','SC','EC','ICE','TGV','EN','NZ','rjx','BUS','HST','Nez','ER',
                                   'CJX','REX','NJ','NT','NLT','EIC','ICB','TLK','EIP','RB','RE','Zr','Peší prechod']):
    """Lists departures or arrivals from station.
    
    The station is given by *uicCode*, number in string format, text for big stations (e.g. "BRATISLAVA").
    The list contains items arriving/departing earliest at datetime *dt*.
    
    Args:
        fromUicCode (str): Uic code of start station.
        toUicCode (str): Uic code of start station.
        dt (datetime, optional): initial datetime of list, defaultly now()
        departure (bool, optional): list departures (True) or arrivals (False), defaultly True
        changes (dict): Changes of connection. Options are whether the connection is direct (True or False),
                        maximal number of changes, minimal and maximal time for change (in minutes)
                        and Uic code of stop to go through. 
        resources (dict): Resources to allocate, i.e. bicycle, wheel chair, bed or baby carriage.
        trainTypes (list): Types of trains to use.
    Returns:
        list: list of departing/arriving trains
    """
    # parse parameters
    dt = _common._parse_date(dt) # UNIX timestamp [ms]
    departure = 'true' if departure else 'false'
    viaStation,viaUicCode = {},changes.get('viaUicCode',None)
    if viaUicCode is not None:
        viaStation['viaStation'] = viaUicCode
    if not isinstance(trainTypes, int):
        trainTypes = meta.TrainType.mask(trainTypes)
    # send request
    connections = _common.get_slovakrail(
        path = f'/api/v2/route', 
        parameters = {
            'fromStation': fromUicCode,
            'toStation': toUicCode,
            **viaStation,
            'departure': departure,
            'travelDate': dt,
            'bed': resources.get('bed',0),
            'bicycle': resources.get('bicycle',0),
            'child': resources.get('child',0),
            'wheelChair': resources.get('wheelChair',0),
            'trainChange': int(changes.get('direct',False)),
            'minChangeTime': changes.get('minTime',4),
            'maxChangeTime': changes.get('maxTime',180),
            'maxChangeCount': changes.get('max',4)
        }
    )
    for conn in connections:
        length = conn['length'] # km
        duration = conn['duration'] # min
        arrivalDt = _common._parse_timestamp(conn['arrivalTimestamp'])
        departureDt = _common._parse_timestamp(conn['departureTimestamp'])
        #infoNext = conn['infoForNextConnection']
        #infoPrev = conn['infoForPreviousConnection']
        for segment in conn['routeSegments']:
            segLength = segment['length']
            segDuration = segment['duration']
            segArrivalDt = _common._parse_timestamp(segment['arrivalTimestamp'])
            segDepartureDt = _common._parse_timestamp(segment['departureTimestamp'])
            segTrainNumber = segment['train']['number']
            segTrainName = segment['train']['name']
            print(f"Train \"{segTrainName}\" [{segTrainNumber}]:")
            for i,stop in enumerate(segment['trainStops']):
                stopArrivalDt = _common._parse_timestamp(stop['arrivalTimestamp'])
                stopDepartureDt = _common._parse_timestamp(stop['departureTimestamp'])
                stopTransfer = stop['transferStation']
                stopUic = stop['trainStation']['uicCode']
                stopName = stop['trainStation']['name']
                print(f"{stopName} [{stopUic}]", end="")
                if i != (len(segment['trainStops']) - 1):
                    print(" - ", end="")
                else:
                    print("\n", end="")
            print("\n")
            
    return connections

__all__ = ["search_connections"]