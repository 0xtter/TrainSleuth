from datetime import datetime
import json
import logging

import yaml

logger = logging.getLogger('project')

SNCF_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
ISO_FORMAT = SNCF_DATE_FORMAT


def from_iso_to_datetime(date: str):
    return datetime.fromisoformat(date)


def get_day_month_year(departure_date: str):
    return from_iso_to_datetime(departure_date).strftime('%d/%m/%Y')


def get_hours_minutes(date: str):
    return from_iso_to_datetime(date).strftime('%H:%M')


def from_iso_to_french(date: str):
    return from_iso_to_datetime(date).strftime('%d/%m/%Y-%H:%M:%S')


def get_iso_date_from_departure_date(departure_date: str):
    return from_iso_to_datetime(departure_date).strftime('%Y-%m-%dT00:00:00')


def parse_yaml_file(configuration_file: str):
    if configuration_file == None:
        logger.error(f'no configuration file provided...')
        return
    logger.debug(f'starting parsing yaml configuration file : {configuration_file}')
    with open(configuration_file) as file:
        try:
            databaseConfig = yaml.safe_load(file)
            logger.debug("yaml file loaded and parsed correctly")
            logger.debug(f'config : {databaseConfig}')
            return databaseConfig
        except yaml.YAMLError as exc:
            logger.error(exc)


