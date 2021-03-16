import requests
from requests.auth import HTTPBasicAuth
import config.credentials as credentials

urlBase = "https://api.rtt.io/api/v1"

def fetch_station_info(station):
    url = "%s/json/search/%s" % (urlBase, station)
    return __request(url)


def __request(url):
    auth = HTTPBasicAuth(credentials.username(), credentials.password())

    response = requests.get(url, auth=auth)

    if response.ok:
        return response.json()
    else:
        return {}