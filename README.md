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

### Lookup station

Lookup stations by prefix with `search_stations()`.
The prefix to match is *case-* and *diacritic- insensitive*.

```python
result = zsr.search_stations('zilina') # get stations with "zilina" prefix
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

Another example

```python
rimavsk_stations = zsr.search_stations('rimavsk')
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

Identifier `uicCode` from Slovak Railways system is used for unique identification of stations.

Station can be looked up with `uicCode`

```python
x = zsr.station("5613206")
```

Since `uicCode` is unique identifier, the result is either single station or an error is raised.
The result for previous call is

```python
{
    'uicCode': '5613206',
    'name': 'Bratislava hl.st.',
    'image': None,
    'latitude': 48.157653,
    'longitude': 17.106339
}
```

### Departures from stations

List the departures from a station with `zsr.departures()`.
The station is specified by `uicCode`.

```python
departures = zsr.departures("5615033") # Rimavská Sobota
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

Arrivals can be returned instead of departures with setting `departure = False`.

Time of departure (or arrival) can be specified as well as second parameter `dt`.

```python
# 3h from now
import datetime
dt = datetime.datetime.now() + datetime.timedelta(hours = 3)
# get trains arriving till 3h from now
rimavska_sobota_arrivals = slovakrailways.departures(5615033, dt, departure=False)
```

The result has form of

```python
[
    {
        'isDeparture': False, # arrival
        'station': 'Tisovec',
        'timestamp': 1597597920000,
        'train': {
            'type': 1,
            'typeList': [1],
            'number': '6729',
            'name': '',
            'features': [
                {
                    'id': 5,
                    'featureDescription': 'Druhá trieda',
                    'featureName': 'Druhá trieda',
                    'order': 0,
                    'reservationType': -1,
                    'reservationName': None,
                    'startStationIndex': None,
                    'stopStationIndex': None
                },
                # ...
                {
                    'id': 104,
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
    }
    # ...
]
```

### Track train

A current train can be tracked for station and delay with

```python
x = zsr.track_train("609")
```

```python
[
    {
        'trainNumber': '609',
        'travelDate': 1597584311000, # [ms] timestamp of issuing the response
        'trainDelay': {
            'previousStationUic': '56-137463-00',
            'previousStationName': 'Piešťany',
            'nextStationUic': '56-138164-00',
            'nextStationName': 'Nové Mesto nad Váhom',
            'currentUic': '56-186874-00',
            'currentName': 'Výh. Horná Streda',
            'delayMinutes': 9,
            'arrivedAtDestination': False,
            'timestamp': 1597584117000 # [ms] timestamp of scheduled departure from next station
        }
    }
]
```

### Connection

Search connections between two stations given by their `uicCode`.

```python
x = zsr.route("5613206","5613600")
```

```python
[
    {
        'id': None,
        'length': 445,
        'duration': 276,
        'arrivalTimestamp': 1597603320000,
        'departureTimestamp': 1597586760000,
        'infoForCurrentConnection': None,
        'timeForCurrentConnection': None,
        'infoForNextConnection': 428253,
        'timeForNextConnection': 1597586760,
        'infoForPreviousConnection': 431702,
        'timeForPreviousConnection': 1597603320,
        'finalOfferExpiration': None,
        'routeSegments': [
            {
                'duration': 276,
                'length': 445,
                'departureTimestamp': 1597586760000,
                'arrivalTimestamp': 1597603320000,
                'trainStops': [
                    {
                        'arrivalTimestamp': 1597586280000,
                        'departureTimestamp': 1597586760000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {
                            'uicCode': '5613206',
                            'name': 'Bratislava hl.st.',
                            'image': None,
                            'latitude': 48.157653,
                            'longitude': 17.106339
                        }
                    },{
                        'arrivalTimestamp': 1597588200000,
                        'departureTimestamp': 1597588260000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {
                            'uicCode': '5613676',
                            'name': 'Trnava',
                            'image': None,
                            'latitude': 48.370911,
                            'longitude': 17.583322
                        }
                    },{
                        'arrivalTimestamp': 1597593180000,
                        'departureTimestamp': 1597593300000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {
                            'uicCode': '5617915',
                            'name': 'Žilina',
                            'image': None,
                            'latitude': 49.21945,
                            'longitude': 18.7408
                        }
                    },{
                        'arrivalTimestamp': 1597599300000,
                        'departureTimestamp': 1597599360000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {
                            'uicCode': '5613250',
                            'name': 'Poprad-Tatry',
                            'image': None,
                            'latitude': 49.051122,
                            'longitude': 20.295414
                        }
                    },{
                        'arrivalTimestamp': 1597602540000,
                        'departureTimestamp': 1597602600000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {'uicCode': '5613560', 'name': 'Kysak', 'image': None, 'latitude': 48.853428, 'longitude': 21.220987}
                    },{
                        'arrivalTimestamp': 1597603320000,
                        'departureTimestamp': None,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {'uicCode': '5613600', 'name': 'Košice', 'image': None, 'latitude': 48.716386, 'longitude': 21.261075}
                    }
                ],
                'previousTrainStops': [
                    {
                        'arrivalTimestamp': None,
                        'departureTimestamp': 1597581720000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {
                            'uicCode': '8101003',
                            'name': 'Wien Hbf',
                            'image': None,
                            'latitude': 0.0,
                            'longitude': 0.0
                        }
                    },{
                        'arrivalTimestamp': 1597584180000,
                        'departureTimestamp': 1597584180000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {'uicCode': '5610046', 'name': 'Kittsee Gr.', 'image': None, 'latitude': 48.11087, 'longitude': 17.111543}
                    },{
                        'arrivalTimestamp': 1597584360000,
                        'departureTimestamp': 1597584540000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {'uicCode': '5614576', 'name': 'Bratislava-Petržalka', 'image': None, 'latitude': 48.11087, 'longitude': 17.111543}
                    },{
                        'arrivalTimestamp': 1597585320000,
                        'departureTimestamp': 1597585920000,
                        'trainStops': True,
                        'transferStation': False,
                        'trainStation': {'uicCode': '5614616', 'name': 'Bratislava-Nové Mesto', 'image': None, 'latitude': 48.167152, 'longitude': 17.136849}
                    }
                ],
                'nextTrainStops': [],
                'availableTicketClasses': None,
                'hasReservation': None,
                'ticketClass': None,
                'train': {
                    'type': 4096,
                    'typeList': [4096],
                    'number': '45',
                    'name': '',
                    'features': [
                        {
                            'id': 86, # luggage storage on train
                            'featureDescription': 'Pojazdná úschovňa batožín',
                            'featureName': 'Preprava batožín',
                            'order': 0,
                            'reservationType': -1,
                            'reservationName': None,
                            'startStationIndex': -1,
                            'stopStationIndex': -1
                        },{
                            'id': 4, # first class
                            'featureDescription': 'Prvá trieda',
                            'featureName': 'Prvá trieda',
                            'order': 1,
                            'reservationType': 5,
                            'reservationName': 'povinná rezervácia miesta',
                            'startStationIndex': -1, 'stopStationIndex': -1
                        },{
                            'id': 5, # second call
                            'featureDescription': 'Druhá trieda',
                            'featureName': 'Druhá trieda',
                            'order': 2,
                            'reservationType': 5,
                            'reservationName': 'povinná rezervácia miesta',
                            'startStationIndex': -1, 'stopStationIndex': -1
                        },{
                            'id': 9, # restaurant wagon
                            'featureDescription': 'Reštauračný alebo bistro vozeň',
                            'featureName': 'Reštauračný alebo bistro vozeň',
                            'order': 3,
                            'reservationType': -1,
                            'reservationName': None,
                            'startStationIndex': -1,
                            'stopStationIndex': -1
                        },{
                            'id': 21, # lift for wheelchair
                            'featureDescription': 'Vo vlaku je radený vozeň so zdvíhacou plošinou a kupé na prepravu imobilných cestujúcich',
                            'featureName': 'Zdvíhacia plošina a oddiel na prepravu invalidov n',
                            'order': 15,
                            'reservationType': 5,
                            'reservationName': 'povinná rezervácia miesta',
                            'startStationIndex': -1,
                            'stopStationIndex': -1
                        },{
                            'id': 22, # wagon for parents and children (up to 10y)
                            'featureDescription': 'Vozeň, alebo kupé vo vozni vyhradené pre cestujúcich s deťmi do 10 rokov',
                            'featureName': 'Oddiel pre cestujúcich s deťmi do 10 rokov',
                            'order': 4,
                            'reservationType': 5,
                            'reservationName': 'povinná rezervácia miesta',
                            'startStationIndex': -1,
                            'stopStationIndex': -1
                        },{
                            'id': 23, # bicycle
                            'featureDescription': 'Preprava bicyklov',
                            'featureName': 'Preprava bicyklov',
                            'order': 5,
                            'reservationType': 21,
                            'reservationName': 'povinná rezervácia',
                            'startStationIndex': -1,
                            'stopStationIndex': -1
                        },{
                            'id': 29, # electric sockets
                            'featureDescription': 'vo vlaku sú radené vozne s prípojkou 230 V',
                            'featureName': 'K dispozícii sú elektrické zásuvky',
                            'order': 12,
                            'reservationType': -1,
                            'reservationName': None,
                            'startStationIndex': -1,
                            'stopStationIndex': -1
                        },{
                            'id': 91, # WiFi
                            'featureDescription': 'V označených vozňoch je v cene cestovného bezdrôtové pripojenie k internetu.',
                            'featureName': 'WiFi pripojenie',
                            'order': 0,
                            'reservationType': -1,
                            'reservationName': None,
                            'startStationIndex': -1,
                            'stopStationIndex': -1
                        },{
                            'id': 103, # skipping a station
                            'featureDescription': 'Vlak v stanici nezastavuje',
                            'featureName': 'Vlak v stanici nezastavuje',
                            'order': 0,
                            'reservationType': -1,
                            'reservationName': None,
                            'startStationIndex': -3,
                            'stopStationIndex': -3
                        },
                        {
                            'id': 171, # train does not wait
                            'featureDescription': 'Vlak nečaká na žiadne prípoje',
                            'featureName': 'Vlak nečaká na žiadne prípoje',
                            'order': 0,
                            'reservationType': -1,
                            'reservationName': None,
                            'startStationIndex': 0,
                            'stopStationIndex': 0
                        }
                    ],
                    'exceptions': [],
                    'carrier': 'Železničná spoločnosť Slovensko, a.s.',
                    'trainDelay': {
                        'previousStationUic': '56-145763-00',
                        'previousStationName': 'Bratislava-Petržalka',
                        'nextStationUic': '56-146167-00',
                        'nextStationName': 'Bratislava-Nové Mesto',
                        'currentUic': '56-132266-00', 'currentName':
                        'Bratislava ústredná nákladná stanic',
                        'delayMinutes': 2,
                        'arrivedAtDestination': False,
                        'timestamp': 1597585080000
                    }
                },
                'finalStation': {
                    'uicCode': '5613600',
                    'name': 'Košice',
                    'image': None,
                    'latitude': 48.716386,
                    'longitude': 21.261075
                }
            }
        ],
        'routeSelfRefs': [
            {'selfRef': 371},
            {'selfRef': -142417112},
            {'selfRef': 251},
            {'selfRef': 3},
            {'selfRef': 182281},
            {'selfRef': 428253},
            {'selfRef': 431702}
        ],
        'passengers': []
    },
    # ...
]
```

Age category and discount can be specified.

```python
route(start, end, dt=None, age_category=103, discount=1)
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


### Meta information

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


## Contribution

Developed by [Martin Benes](https://github.com/martinbenes1996).

Join on [GitHub](https://github.com/martinbenes1996/slovakrailways).
