from datetime import datetime
import json
import requests
import logging

from modules.data_parser.data_parser import get_iso_date_from_departure_date

logger = logging.getLogger('project')

SNCF_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
DEFAULT_HEADERS = {
    'Host': 'www.maxjeune-tgvinoui.sncf',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'application/json',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.maxjeune-tgvinoui.sncf/sncf-connect/max-planner',
    'Content-Type': 'application/json',
    'x-client-app': 'MAX_JEUNE',
    'x-client-app-version': '1.35.4',
    'x-distribution-channel': 'OUI',
    'Origin': 'https://www.maxjeune-tgvinoui.sncf',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers'
}

DEFAULT_URL = 'https://www.maxjeune-tgvinoui.sncf/api/public/refdata/search-freeplaces-proposals'
# Liste des gares disponibles ici https://www.maxjeune-tgvinoui.sncf/api/public/refdata/freeplaces-stations?label=lil


class TrainRequest:
    def __init__(self, origin: str, destination: str, departure_date: str, request_url: str = DEFAULT_URL, request_headers: dict = DEFAULT_HEADERS):
        self.request_url = request_url
        self.request_data = {
            "departureDateTime": f"{get_iso_date_from_departure_date(departure_date)}",
            "destination": f"{destination}",
            "origin": f"{origin}"
        }
        self.request_headers = request_headers

    def update_response(self):
        logger.debug(
            f"Requesting {self.request_url} with data : {self.request_data}")
        response = requests.post(
            self.request_url, headers=self.request_headers, json=self.request_data)

        logger.debug(f"Request sent sucessfully!")

        if response.status_code == 200:
            logger.debug(
                f"Response received sucessfully! request content : {response.json()}")
            self.response_raw = response.json()
            self.parse_raw_response()
            return True
        elif response.status_code == 404:
            logger.debug(
                f"The request failed with error code {response.status_code}, train probably more than 30 days away or already passed...")
        else:
            logger.error(
                f"The request failed with error code {response.status_code}")
        self.response_raw = None
        self.updatedAt = None
        self.expiresAt = None
        self.freePlacesRatio = None
        self.proposals = []
        return False

    def parse_raw_response(self):
        logger.debug("parsing datas from raw response")

        self.updatedAt = datetime.fromtimestamp(
            self.response_raw['updatedAt'] / 1000).strftime(SNCF_DATE_FORMAT)
        self.expiresAt = self.response_raw['expiresAt']
        self.freePlacesRatio = self.response_raw['freePlacesRatio']
        self.proposals = self.response_raw['proposals']

    def get_updated_time(self):
        return self.updatedAt

    def get_proposals(self):
        logger.debug("parsing proposals from raw response")
        return self.proposals

    def get_all_trains_in_day(self):
        return self.proposals

    def get_trains_before(self, departure_date: str, proposals: list = None):
        if proposals is None:
            proposals = self.proposals

        departure_datetime = datetime.strptime(
            departure_date, '%Y-%m-%dT%H:%M:%S')
        trains_before = []
        for proposal in proposals:
            train_departure = datetime.fromisoformat(proposal['departureDate'])
            if train_departure <= departure_datetime:
                trains_before.append(proposal)
        return trains_before

    def get_trains_after(self, departure_date: str, proposals: list = None):
        if proposals is None:
            proposals = self.proposals
        
        departure_datetime = datetime.strptime(
            departure_date, '%Y-%m-%dT%H:%M:%S')
        trains_after = []
        for proposal in proposals:
            train_departure = datetime.fromisoformat(proposal['departureDate'])
            if train_departure >= departure_datetime:
                trains_after.append(proposal)
        return trains_after

    def get_trains_between(self, departure_date_from: str, departure_date_to: str):
        return self.get_trains_after(departure_date_from, self.get_trains_before(departure_date_to))
    
    def get_precise_train(self,deparure_date: str):
        return self.get_trains_between(deparure_date,deparure_date)
