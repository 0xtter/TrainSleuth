from datetime import datetime
import logging.config
import os
import sys
import time

import argparse
from modules.Notifications.Telegram.telegram_notificator import TelegramNotify
from modules.Sleuth.Sleuth import Sleuth

from modules.data_parser.data_parser import parse_yaml_file

DELAY_CHECK_CONFIGURATION_FILE=5
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

def setup_logger():
    global logger
    global file_logger
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('project')
    logger.debug("Logger 'project' started correctly")
    
    file_logger = logging.getLogger('file_logger')
    fh = logging.FileHandler('logs/trainSleuth_{:%Y-%m-%d}.log'.format(datetime.now()))
    file_logger.addHandler(fh)
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

    return args

def sleuth_train(args):
    last_modified = -1
    config_file = args.config
    
    while True:
        # Check if configuration file was modified
        if os.path.getmtime(config_file) > last_modified:
            try:
                logger.info(f'modification in configuration "{config_file}" file detected')
                
                config=parse_yaml_file(config_file)

                # update notifications
                if config['notification'].get('telegram') != None:
                    TelegramNotify.update_configuration(config['notification']['telegram'])
                    telegram_alert = TelegramNotify()
                    telegram_alert.send_telegram_message(f'modification in configuration "{config_file}" file detected')
                    
                # update sleuths
                sleuths = []
                for train in config['trains']:
                    sleuths.append(Sleuth(train))
                
                last_modified = os.path.getmtime(config_file)
            except Exception as e:
                logger.error(f'error in configuration file, make sure you followed the correct syntax... Error : {e}')
                time.sleep(DELAY_CHECK_CONFIGURATION_FILE)
                continue
        
        # Wait for interval seconds (including the execution time)
        print(LINE_UP, end=LINE_CLEAR)
        for sleuth in sleuths:
            try:
                sleuth.request_trains()
                sleuth.show_results()
            except Exception as e:
                logger.error(f'Error occurred while requesting and showing corresponding trains of Sleuth : {sleuth.name}: {e}')
        
        if args.one_time == True:
            break

        logger.info(f'Requesting with {args.interval}s interval SNCF API... Requests ID : {sleuths[0].nb_requests}')
        time.sleep(args.interval - time.time() % args.interval)


if __name__ == '__main__':
    try:
        setup_logger()
        args = parse_args()
        sleuth_train(args)
    except KeyboardInterrupt:
        print("Stopped by user. Thanks for using TrainSleuth.\n")
