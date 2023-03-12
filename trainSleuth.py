from datetime import datetime
import logging.config
from modules.SNCF_API import sncfAPI
import argparse


def setup_logger():
    global logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('project')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    if args.verbose == True:
        logger.handlers[0].setLevel(logging.DEBUG)
        logger.debug("Verbose mode activated")


if __name__ == '__main__':
    setup_logger()
    parse_args()
    
    origin="FRPNO"
    destination="FRADJ"
    departure_date="2023-03-15T17:00:00"

    trains = sncfAPI.get_trains_after(origin, destination,departure_date)

    last_update=datetime.fromtimestamp(trains["updatedAt"] / 1000).strftime('%d/%m/%Y à %H:%M')

    print(f"Liste des trains le {datetime.strptime(departure_date, '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y')} (Dernière mise a jour : {last_update})")

    for proposal in trains["proposals"]:
        # Convertir la chaîne de caractères en objet datetime
        date_time_obj = datetime.strptime(proposal['departureDate'], '%Y-%m-%dT%H:%M')

        # Formater la date et l'heure dans un format plus lisible
        formatted_date_time = date_time_obj.strftime('%H:%M')
        print(f"Train allant de {proposal['origin']['label']} vers {proposal['destination']['label']} de {formatted_date_time} à {proposal['freePlaces']} places disponibles")
