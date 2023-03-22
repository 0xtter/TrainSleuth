from datetime import datetime
import logging

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
