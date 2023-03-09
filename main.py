import requests

url = 'https://www.maxjeune-tgvinoui.sncf/api/public/refdata/search-freeplaces-proposals'
headers = {
    'Host': 'www.maxjeune-tgvinoui.sncf',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'application/json',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.maxjeune-tgvinoui.sncf/sncf-connect/max-planner',
    'Content-Type': 'application/json',
    'x-syg-correlation-id': 'b3f3e9e6-56f1-4d97-8b63-d55391d7ee34',
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
data = {
    "departureDateTime":"2023-03-15T00:00:00",
    "destination":"FRADJ",
    "origin":"FRPNO"
}

response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    trains = response.json()
    print(trains)
else:
    print("La requête a échoué avec le code d'erreur", response.status_code)
