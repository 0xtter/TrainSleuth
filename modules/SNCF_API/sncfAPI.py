import requests
import logging

logger = logging.getLogger('project')

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

DEFAULT_URL='https://www.maxjeune-tgvinoui.sncf/api/public/refdata/search-freeplaces-proposals'
# Liste des gares disponibles ici https://www.maxjeune-tgvinoui.sncf/api/public/refdata/freeplaces-stations?label=lil

def request_api( headers: dict, data: dict, url :str = "https://www.maxjeune-tgvinoui.sncf/api/public/refdata/search-freeplaces-proposals"):
    logger.debug(f"Requesting {url} with data : {data}")

    response = requests.post(url, headers=headers, json=data)

    logger.debug(f"Request sent sucessfully!")

    if response.status_code == 200:
        logger.debug(f"Response received sucessfully! request content : {response.json()}")
        return response.json()
    else:
        logger.error(f"The request failed with error code {response.status_code}")
        return None



def get_trains_after(origin: str, destination: str, departure_date_time: str):

    data = {
        "departureDateTime":f"{departure_date_time}",
        "destination":f"{destination}",
        "origin":f"{origin}"
    }

    return request_api(DEFAULT_HEADERS,data)