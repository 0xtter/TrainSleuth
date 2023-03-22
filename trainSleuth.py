import logging.config
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
        "Date (UTC) | Logger | Train departure date | Origin | Destination | Seats available")


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


def log_train_data(date: str, origin: str, destination: str, available_seats: int):
    file_logger.info(f"{date} | {origin} | {destination} | {available_seats}")


def one_time():
    sleuth = Sleuth("configurations/train_1.example.yaml")
    # origin = "FRPNO"
    # destination = "FRADJ"
    # departure_date = "2023-03-22T17:00:00"

    # trainRequest = sncfAPI.TrainRequest(origin, destination, departure_date)

    # logger.info(
    #     f"Liste des trains le {get_day_month_year(departure_date)} (Dernière mise a jour : {from_iso_to_french(trainRequest.updatedAt)})")

    # for proposal in trainRequest.get_trains_between("2023-03-23T10:00:00","2023-03-23T15:00:00"):
    #     # Convertir la chaîne de caractères en objet datetime
    #     departure_date = proposal['departureDate']
    #     log_train_data(departure_date, proposal['origin']['label'],
    #                    proposal['destination']['label'], proposal['freePlaces'])

    #     logger.info(
    #         f"Train allant de {proposal['origin']['label']} vers {proposal['destination']['label']} de {get_hours_minutes(departure_date)} à {proposal['freePlaces']} places disponibles")


if __name__ == '__main__':
    setup_logger()
    parse_args()
