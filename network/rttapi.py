import requests
from requests.auth import HTTPBasicAuth
from config.credentials import Credentials

urlBase = "https://api.rtt.io/api/v1"

def fetch_station_info(station):
    url = "{base}/json/search/{station}".format(base=urlBase, station=station)
    return __request(url)

def fetch_service_info(service_uid, service_date):
    url = "{base}/json/service/{service_uid}/{year}/{month}/{day}".format(
        base=urlBase,
        service_uid=service_uid,
        year=service_date.strftime('%Y'),
        month=service_date.strftime('%m'),
        day=service_date.strftime('%d')
    )
    return __request(url)


def __request(url):
    credentials = Credentials()
    auth = HTTPBasicAuth(credentials.username, credentials.password)

    response = requests.get(url, auth=auth)

    if response.ok:
        return response.json()
    else:
        return {}