import logging.config
import time

import yaml
from modules.SNCF_API import sncfAPI
import argparse
from modules.Sleuth.Sleuth import Sleuth

from modules.data_parser.data_parser import from_iso_to_french, get_day_month_year, get_hours_minutes, parse_yaml_file


def setup_logger():
    global logger
    global file_logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('project')
    logger.debug("Logger 'project' started correctly")
    file_logger = logging.getLogger('file_logger')
    logger.debug("Logger 'file_logger' started correctly")
    file_logger.info(
        "Date (UTC) | SleuthName | Request ID | Train departure date | Origin | Destination | Seats available")


def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--one-time", help="execute the research only one time", action="store_true")
    group.add_argument(
        "--interval", help="time interval (in seconds) between every refresh", type=int, nargs='?', default=10)

    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument(
        "--config", help="path to the configuration file", type=str, nargs='?', default='./configurations/trains.example.yaml')
    
    args = parser.parse_args()

    if args.verbose == True:
        logger.handlers[0].setLevel(logging.DEBUG)
        logger.debug("Verbose mode activated")

    if args.one_time == True:
        one_time(args.config)
        return
    else:
        sleuth_train(args.config, args.interval)


def one_time(config_file: str):
    sleuths_config=parse_yaml_file(config_file)
    for train in sleuths_config['trains']:
        sleuth = Sleuth(train)
        sleuth.request_trains()
        sleuth.show_results()

def sleuth_train(config_file: str, interval: int):
    sleuths_config=parse_yaml_file(config_file)
    sleuths = []
    # Wait for interval seconds (including the execution time)
    for sleuth in sleuths_config['trains']:
        sleuths.append(Sleuth(train))
    while True:
        sleuths_config=parse_yaml_file(config_file)
        # Wait for interval seconds (including the execution time)
        for train in sleuths_config['trains']:
            sleuth.update_configuration(train)
            sleuth.request_trains()
            sleuth.show_results()
            
        time.sleep(interval - time.time() % interval)


if __name__ == '__main__':
    setup_logger()
    parse_args()
