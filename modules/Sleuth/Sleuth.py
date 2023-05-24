from datetime import datetime
from modules.Notifications.Telegram.telegram_notificator import TelegramNotify
from modules.SNCF_API import sncfAPI
import logging

from modules.data_parser.data_parser import from_iso_to_french, get_day_month_year, get_hours_minutes


logger = logging.getLogger('project')
file_logger = logging.getLogger('file_logger')

MAX_REQUEST_ID = 1000000


def log_train_data(request_id: int, sleuth_name: str, date: str, origin: str, destination: str, available_seats: int):
    file_logger.info(
        f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')} | {request_id} |{sleuth_name} | {date} | {origin} | {destination} | {available_seats}")


class Sleuth():
    def __init__(self, configuration: dict):
        logger.debug(f'creating new Sleuth with configuration : {configuration}')
        self.update_configuration(configuration)
        self.trainRequest = sncfAPI.TrainRequest(
            self.origin, self.destination, self.departure_date)
        self.nb_requests = 0
        self.last_proposals = {}

    def update_configuration(self,configuration: dict):
        self.configuration = configuration
        self.name = self.configuration['name']
        self.type = self.configuration['type']
        self.origin = self.configuration['origin']
        self.destination = self.configuration['destination']
        self.departure_date = self.configuration['departure_date']

    def request_trains(self):
        self.trainRequest.update_response()
        self.nb_requests = (self.nb_requests + 1) % MAX_REQUEST_ID

    def show_proposal(self, proposal: dict):
        log_train_data(self.nb_requests, self.name, proposal['departureDate'], proposal['origin']['label'],
                    proposal['destination']['label'], proposal['freePlaces'])
        telegram_alert = TelegramNotify()
        telegram_alert.send_telegram_message(f"{self.name} (Le {get_day_month_year(self.departure_date)} maj à {from_iso_to_french(self.trainRequest.updatedAt)}, requestID : {self.nb_requests}) : Train de {proposal['origin']['label']:<15} vers {proposal['destination']['label']:<18} de {get_hours_minutes(proposal['departureDate'])} à {proposal['freePlaces']:<2} places disponibles")
        logger.info(
            f"{self.name} (Le {get_day_month_year(self.departure_date)} maj à {from_iso_to_french(self.trainRequest.updatedAt)}, requestID : {self.nb_requests}) : Train de {proposal['origin']['label']:<15} vers {proposal['destination']['label']:<18} de {get_hours_minutes(proposal['departureDate'])} à {proposal['freePlaces']:<2} places disponibles")

    def show_results(self,proposals: list = 0):
        proposals = self.trainRequest.get_precise_train(self.departure_date+":00")

        current_proposals = {}
        for proposal in proposals:
            if proposal['departureDate'] not in self.last_proposals:
                current_proposals[proposal['departureDate']] = proposal['freePlaces']
                self.show_proposal(proposal)
            elif self.last_proposals[proposal['departureDate']] != proposal['freePlaces']:
                current_proposals[proposal['departureDate']] = proposal['freePlaces']
                self.show_proposal(proposal)
            else:
                current_proposals[proposal['departureDate']] = proposal['freePlaces']
                continue
        self.last_proposals=current_proposals
            