# TrainSleuth

Ce projet utilise l'API de la SNCF pour trouver automatiquement des trains TGV MAX disponibles. Il permettra aux utilisateurs de rechercher facilement et rapidement des horaires TGV MAX pour planifier leurs voyages en train.

# Installation

```shell
pip install -r requirements.txt
```

# Configuration file

You first need to write your own configuration file in `configurations/trains.example.yaml` 

like following:

```yaml
# example of configuration file

trains:
  - name: Name of your train (can be whatever you want)
    type: train   # search for a particular train
    departure_date: 2023-04-05T20:25 # Date of departure of your train (make sure the time is corresponding to an existing train)
    origin: FRPNO # The origin station (see Liste gares TGV MAX.md)
    destination: FRADJ # The destination station (see Liste gares TGV MAX.md)
  
  - name: Name of your train (can be whatever you want)
    type: before    # all trains before departure date
    departure_date: 2023-07-05T20:30
    origin: FRPNO
    destination: FRADJ
  
  - name: Name of your train (can be whatever you want)
    type: after    # all trains after departure date
    departure_date: 2023-07-05T07:25
    origin: FRPNO
    destination: FRADJ

notification:
    telegram:
      API_KEY: "YOUR-KEY" # Follow steps here : https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot
      user_id_to_notify: "YOUR-USER-ID" # To get your id use : https://web.telegram.org/a/#1157763503
      message_format: "SYMBOL TRAIN_DATE à TRAIN_DEPARTURE_TIME (TRAIN_NAME) - TRAIN_ORIGIN > TRAIN_DESTINATION | TRAIN_FREE_PLACES_LEFT places restantes  (MAJ: UPDATE_DATETIME, requestID: REQUEST_NUMBER)"
      symbol_less_5_places_left: "🔴"
      symbol_6_to_10_places_left: "🟠"
      symbol_11_to_20_places_left: "🔵"
      symbol_more_20_places_left: "🟢"
```

Note that you can change notification message by editing the value of `message_format`. Variables are :

- `SYMBOL`: character to display according to the number of remaining seats.
- `TRAIN_NAME`: this is the name of the train you set in your config file 
- `TRAIN_DATE`: DD/MM/YYYY
- `TRAIN_DEPARTURE_TIME`: HH:MM
- `TRAIN_ORIGIN`: Origin station
- `TRAIN_DESTINATION`: Destination station
- `TRAIN_FREE_PLACES_LEFT`: Number of remaining free seats
- `REQUEST_NUMBER`: the n-th request since the program started
- `UPDATE_DATETIME`: update timedate

You do not need to use all variables.

# Usage

Save your configuration file and start `trainSleuth.py`:

```shell
python trainSleuth.py
```

This will start script with default values. If you want to customise it yourself, see :

```shell
python trainSleuth.py --help
```

```
usage: trainSleuth.py [-h] [--one-time | --interval [INTERVAL]] [-v] [--config [CONFIG]]

options:
  -h, --help            show this help message and exit
  --one-time            execute the research only one time
  --interval [INTERVAL]
                        time interval (in seconds) between every refresh
  -v, --verbose         increase output verbosity
  --config [CONFIG]     path to the configuration file
```
