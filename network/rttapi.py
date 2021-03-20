import requests
from requests.auth import HTTPBasicAuth
from config.credentials import Credentials

urlBase = "https://api.rtt.io/api/v1"

def fetch_station_info(station):
    url = "%s/json/search/%s" % (urlBase, station)
    return __request(url)

def fetch_service_info(service_uid, service_date):
    url = "%s/json/service/%s/%s/%s/%s" % (urlBase, service_uid, service_date.strftime('%Y'), service_date.strftime('%m'), service_date.strftime('%d'))
    print(url)
    return __request(url)


def __request(url):
    credentials = Credentials()
    auth = HTTPBasicAuth(credentials.username, credentials.password)

    response = requests.get(url, auth=auth)

    if response.ok:
        return response.json()
    else:
        return {}