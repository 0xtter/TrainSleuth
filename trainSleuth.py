import logging.config

import yaml
from modules.SNCF_API import sncfAPI
import argparse
from modules.Sleuth.Sleuth import Sleuth

from modules.data_parser.data_parser import from_iso_to_french, get_day_month_year, get_hours_minutes


def setup_logger():
    global logger
    global file_logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('project')
    logger.debug("Logger 'project' started correctly")
    file_logger = logging.getLogger('file_logger')
    logger.debug("Logger 'file_logger' started correctly")
    file_logger.info(
        "Date (UTC) | SleuthName | Train departure date | Origin | Destination | Seats available")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity", action="store_true")
    parser.add_argument(
        "--one-time", help="execute the research only one time", action="store_true")
    args = parser.parse_args()
    if args.verbose == True:
        logger.handlers[0].setLevel(logging.DEBUG)
        logger.debug("Verbose mode activated")
    if args.one_time == True:
        one_time()




def one_time():
    configuration_file = "configurations/train_1.example.yaml"
    with open(configuration_file) as file:
        try:
            databaseConfig = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)

    for train in databaseConfig['trains']:
        sleuth = Sleuth(train) 
    

if __name__ == '__main__':
    setup_logger()
    parse_args()
