# TrainSleuth

Ce projet utilise l'API de la SNCF pour trouver automatiquement des trains TGV MAX disponibles. Il permettra aux utilisateurs de rechercher facilement et rapidement des horaires TGV MAX pour planifier leurs voyages en train.

# Installation

```shell
pip install -r requirements.txt
```

# Usage

You first need to write your own configuration file in `configurations/trains.example.yaml` 

like following:

```yaml
trains:
  - name: Name of your train (can be whatever you want)
    type: train # For the moment, only 'train' is supported --> check for a specific train
    departure_date: 2023-04-05T20:25 # Date of departure of your train (make sure the time is corresponding to an existing train)
    origin: FRPNO # The origin station (see Liste gares TGV MAX.md)
    destination: FRADJ # The destination station (see Liste gares TGV MAX.md)
```

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