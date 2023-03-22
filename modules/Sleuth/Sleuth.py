from datetime import datetime
from modules.SNCF_API import sncfAPI
import logging

from modules.data_parser.data_parser import from_iso_to_french, get_day_month_year, get_hours_minutes


logger = logging.getLogger('project')
file_logger = logging.getLogger('file_logger')

def log_train_data(sleuth_name: str, date: str, origin: str, destination: str, available_seats: int):
    file_logger.info(f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')} | {sleuth_name} | {date} | {origin} | {destination} | {available_seats}")



class Sleuth():
    def __init__(self, configuration: dict):
        self.configuration = configuration
        self.update_configuration()

    def update_configuration(self):
        self.name = self.configuration['name']
        self.type = self.configuration['type']
        self.origin = self.configuration['origin']
        self.destination = self.configuration['destination']
        self.departure_date = self.configuration['departure_date']
        self.trainRequest = sncfAPI.TrainRequest(self.origin, self.destination, self.departure_date)
        self.show_results()
    
    def show_results(self):
        logger.info(
        f"Liste des trains le {get_day_month_year(self.departure_date)} (Dernière mise a jour : {from_iso_to_french(self.trainRequest.updatedAt)})")

        for proposal in self.trainRequest.get_trains_before(self.departure_date+":00"):
            # Convertir la chaîne de caractères en objet datetime
            departure_date = proposal['departureDate']
            log_train_data(self.name,departure_date, proposal['origin']['label'],
                        proposal['destination']['label'], proposal['freePlaces'])

            logger.info(
                f"Train allant de {proposal['origin']['label']} vers {proposal['destination']['label']} de {get_hours_minutes(departure_date)} à {proposal['freePlaces']} places disponibles")


