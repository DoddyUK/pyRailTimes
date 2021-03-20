import requests
from requests.auth import HTTPBasicAuth
from config.credentials import Credentials

class RttApi:
    urlBase = "https://api.rtt.io/api/v1"
    credentials = Credentials()

    def fetch_station_info(self, station):
        url = "{base}/json/search/{station}".format(base=self.urlBase, station=station)
        return self.__request(url)

    def fetch_service_info(self, service_uid, service_date):
        url = "{base}/json/service/{service_uid}/{year}/{month}/{day}".format(
            base=self.urlBase,
            service_uid=service_uid,
            year=service_date.strftime('%Y'),
            month=service_date.strftime('%m'),
            day=service_date.strftime('%d')
        )
        return self.__request(url)

    def __request(self, url):
        auth = HTTPBasicAuth(self.credentials.username, self.credentials.password)

        response = requests.get(url, auth=auth)

        if response.ok:
            return response.json()
        else:
            return {}


