# slovakrailways

Python envelope of Slovak Railways API

## Installation

Install the package simply typing

```bash
pip install slovakrailways
```

Import into Python3 with

```python
import slovakrailways as zsr
```

And you're good to go. Btw ZSR is an abbreviation of Slovak railways.

## Usage

### Get station information

Get information of station with function `zsr.station()`, taking the prefix of the name.
The prefix to match is *case-* and *diacritic- insensitive*.

```python
result = zsr.stations('zilina') # get stations with "zilina" prefix
```

Result has following structure.

```python
[
    {
        "uicCode": "5617915",
        "name": "Žilina",
        "image": None,
        "latitude": 49.21945,
        "longitude": 18.7408
    },{
        "uicCode": "5617930",
        "name": "Žilina-Solinky",
        "image": None,
        "latitude": 49.198517,
        "longitude": 18.736596
    },{
        "uicCode": "5617925",
        "name": "Žilina-Záriečie",
        "image": None,
        "latitude": 49.218306,
        "longitude": 18.730756
    }
]
```

Identifier *uicCode* from Slovak Railways system is used for unique identification,
in the package it is references as *uic_code*.

```python
rimavsk_stations = zsr.stations('rimavsk')
```

```python
[
    {
        "uicCode": "5615293",
        "name": "Rimavská Baňa",
        "image": None,
        "latitude": 48.511147,
        "longitude": 19.941259
    },{
        "uicCode": "5615213",
        "name": "Rimavská Píla",
        "image": None,
        "latitude": 48.650532,
        "longitude": 19.944147
    },{
        "uicCode": "5615033",
        "name": "Rimavská Sobota",
        "image": None,
        "latitude": 48.38123,
        "longitude": 20.019545
    },{
        # ...
    },{
        "uicCode": "5615303", 
        "name": "Rimavské Zalužany",
        "image": None,
        "latitude": 48.500525,
        "longitude": 19.935475
    }
]
```

### Get departures from station

Station is identified by the *uicCode*.
List the departures from a station with `zsr.departures()`,
which takes the uic_code as first parameter

```python
# get uic_code of Rimavska Sobota station
uic_code = zsr.stations('rimavska sobota')[0]['uicCode']
print(uic_code) # "5615033"
# get current departures
departures = zsr.departures(uic_code)
```

The *departures* has following structure

```python
[
    {
        "isDeparture": True,
        "station": "Fiľakovo",
        "timestamp": 1587662220000,
        "train": {
            "type": 1,
            'typeList': [1],
            'number': '6258',
            'name': '',
            'features': [
                { 
                    'id': 5, # second class
                    'featureDescription': 'Druhá trieda',
                    'featureName': 'Druhá trieda',
                    'order': 0,
                    'reservationType': -1,
                    'reservationName': None,
                    'startStationIndex': None,
                    'stopStationIndex': None
                },{
                    'id': 23, # bike 
                    'featureDescription': 'Preprava bicyklov', 
                    'featureName': 'Preprava bicyklov',
                    'order': 0,
                    'reservationType': -1,
                    'reservationName': None,
                    'startStationIndex': None,
                    'stopStationIndex': None
                },{
                    'id': 107, # tickets without integrated reservation
                    'featureDescription': 'SCIC NRT tarifa bez integrovanej rezervácie',
                    'featureName': 'SCIC NRT tarifa',
                    'order': 0,
                    'reservationType': -1,
                    'reservationName': None,
                    'startStationIndex': None,
                    'stopStationIndex': None
                },{
                    'id': 101, # stops on demand
                    'featureDescription': 'Vlak zastavuje len na znamenie, alebo požiadanie',
                    'featureName': 'Zastavenie na znamenie',
                    'order': 0,
                    'reservationType': -1,
                    'reservationName': None,
                    'startStationIndex': None,
                    'stopStationIndex': None
                }
            ],
            'exceptions': [],
            'carrier': 'Železničná spoločnosť Slovensko, a.s.',
            'trainDelay': None
        }
    },
    {
        # ...
    }
]
```

Specify time of departure (or arrival)

```python
# 3h from now
import datetime
dt = datetime.datetime.now() + datetime.timedelta(hours = 3)
# get trains arriving till 3h from now
rimavska_sobota_arrivals = slovakrailways.departures(uic_code, dt, departures=False)
```

```python
# todo: output
```

Get delay.

```python
delay(train_number) # dt=None
```

```python
# todo: output
```

Get route between two points.

```python
route(start, end, dt=None, departure=False)
```

```python
# todo: output
```

Get route between two points, specify age category and discount.

```python
route(start, end, dt=None, age_category=103, discount=1)
```

```python
# todo: output
```

Get pricing of route by

```python
pricing(route_reference, age_category=103, discount=1, free=True)
```

```python
# todo: output
```

Implicitly the pricing is for adult without any discount.
Free ticket must be requested explicitly (by `free=True`).

### Get meta information

Check whether API is working by *zsr.meta.status()*.
Function returns True or False.

```python
assert zsr.meta.status()
```

List avaliable discounts for various age categories with *zsr.meta.age_categories()*.

```python
age_categories = zsr.meta.age_categories()
```

The format of output is

```python
[
    {
        'id': 100, # children 0 - 5y
        'fromAge': 0, 'toAge': 5,
        'description': 'Dieťa (0 - 5 r.)',
        'availableDiscounts': [
            # no discount
            {'id': 1, 'description': 'Bez zľavy', 'documentRequired': False, 'freeTransportAvailable': False},
            # international
            {'id': 613, 'description': 'Medzinárodný lístok/ Interrail', 'documentRequired': False, 'freeTransportAvailable': False}
        ]
    },{
        'id': 101, # children 6 - 15y
        'fromAge': 6, 'toAge': 15,
        'description': 'Dieťa (6 - 15 r.)',
        'availableDiscounts': [
            # no discount
            {'id': 1, 'description': 'Bez zľavy', 'documentRequired': False, 'freeTransportAvailable': False},
            # student
            {'id': 600, 'description': 'Preukaz pre žiaka/Študenta', 'documentRequired': False, 'freeTransportAvailable': True},
            {'id': 601, 'description': 'Držiteľ trať. lístka - študent', 'documentRequired': False, 'freeTransportAvailable': False},
            # disabled
            {'id': 607, 'description': 'Preukaz ŤZP', 'documentRequired': False, 'freeTransportAvailable': False},
            {'id': 608, 'description': 'Preukaz ŤZP-S', 'documentRequired': False, 'freeTransportAvailable': False},
            {'id': 609, 'description': 'Sprievodca ŤZP-S', 'documentRequired': False, 'freeTransportAvailable': False},
            # railway card
            {'id': 610, 'description': 'Železničný preukaz ČD', 'documentRequired': False, 'freeTransportAvailable': False},
            {'id': 611, 'description': 'Železničný preukaz SR', 'documentRequired': False, 'freeTransportAvailable': False},
            # international
            {'id': 613, 'description': 'Medzinárodný lístok/ Interrail', 'documentRequired': False, 'freeTransportAvailable': False},
            # child card
            {'id': 614, 'description': 'Preukaz pre dieťa do 16 r.', 'documentRequired': False, 'freeTransportAvailable': True},
            # ISIC (slovak schools)
            {'id': 617, 'description': 'ISIC aktivovaný školou v SR', 'documentRequired': False, 'freeTransportAvailable': True}
        ]
    },{
        'id': 102, # youngster 16 - 25y
        'fromAge': 16, 'toAge': 25,
        # ...
    },{
        'id': 103, # adult 26 - 61y 
        'fromAge': 26, 'toAge': 61,
        # ...
    },{
        'id': 104, # adult 62 - 69y
        'fromAge': 62, 'toAge': 69,
        # ...
    },{
        'id': 105, # adult 70y+
        'fromAge': 70, 'toAge': 999,
        # ...
    }
]
```

List train types of ZSR by *zsr.meta.train_types()*.

```python
train_types = zsr.meta.train_types()
```

The output has format such as

```python
[
    {'value': 1, 'name': 'Os', 'description': 'osobný vlak'}, # regular (local) train
    {'value': 2, 'name': 'RR', 'description': 'Regionálny rýchlik'}, # regional "fast train"
    {'value': 4, 'name': 'R', 'description': 'rýchlik'}, # "fast train"
    {'value': 8, 'name': 'IR', 'description': 'IR'},
    {'value': 16, 'name': 'Ex', 'description': 'expresný vlak'}, # express
    # ...
    {'value': 137438953472, 'name': 'RB', 'description': 'Regionalbahn'},
    {'value': 274877906944, 'name': 'RE', 'description': 'Regional-Express'},
    {'value': 36028797018963968, 'name': 'Peší prechod', 'description': 'peší presun'} # on foot
]
```

List all possible attributes place can have by

```python
place_attributes = zsr.meta.place_attributes()
```

The format of place attributes is

```python
[
    {'description': 'vozeň s kupé', 'id': 1}, # compartment
    {'description': 'vozeň veľkopriestorový', 'id': 2}, # open-type
    {'description': 'Miesto pri stolíku', 'id': 3}, # with table
    {'description': 'Miesto so zásuvkou', 'id': 5}, # with socket
    {'description': 'Miesto s WIFI', 'id': 6}, # with wifi
    {'description': 'Miesto v smere jazdy', 'id': 7}, # facing forward
    {'description': 'Miesto proti smeru jazdy', 'id': 8}, # facing backwards
    {'description': 'Miesto pre cest. s inv.vozíkom', 'id': 9}, # wheelchair user
    {'description': 'Miesto pre spriev.s inv.voz.', 'id': 10} # accompany of wheelchair user
]
```
