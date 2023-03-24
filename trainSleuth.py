import logging.config
import os
import time

import yaml
from modules.SNCF_API import sncfAPI
import argparse
from modules.Sleuth.Sleuth import Sleuth

from modules.data_parser.data_parser import from_iso_to_french, get_day_month_year, get_hours_minutes, parse_yaml_file

DELAY_CHECK_CONFIGURATION_FILE=5

def setup_logger():
    global logger
    global file_logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('project')
    logger.debug("Logger 'project' started correctly")
    file_logger = logging.getLogger('file_logger')
    logger.debug("Logger 'file_logger' started correctly")
    file_logger.info(
        "Date (UTC) | Request ID | SleuthName | Train departure date | Origin | Destination | Seats available")


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

    sleuth_train(args.config, args)

def sleuth_train(config_file: str, args):
    last_modified = -1
    
    while True: 
        if os.path.getmtime(config_file) > last_modified:
            try:
                logger.info(f'modification in configuration "{config_file}" file detected')
                sleuths = []
                sleuths_config=parse_yaml_file(config_file)
                for train in sleuths_config['trains']:
                    sleuths.append(Sleuth(train))
                last_modified = os.path.getmtime(config_file)
            except Exception as e:
                logger.error(f'error in configuration file, make sure you followed the correct syntax... Error : {e}')
                time.sleep(DELAY_CHECK_CONFIGURATION_FILE)
                continue
        else: 
            time.sleep(args.interval - time.time() % args.interval)
            # Wait for interval seconds (including the execution time)
            for sleuth in sleuths:
                sleuth.request_trains()
                sleuth.show_results()

        if args.one_time == True:
            break


if __name__ == '__main__':
    setup_logger()
    parse_args()
