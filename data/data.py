import datetime
from rttapi.api import RttApi
from rttapi.model import SearchResult, LocationContainer
from config.credentials import Credentials
from typing import List

class StationData:
    data: SearchResult = None
    last_update: datetime.datetime = None
    station_name: str = None
    services: List[LocationContainer] = None
    __changeDelta = datetime.timedelta(minutes=1) # Minimum time between API requests

    def __init__(self, station_code):
        self.__station_code = station_code
        credentials = Credentials()
        self.__api = RttApi(credentials.username, credentials.password)

    def check_updates(self, updated_callback):
        if self.data is None \
                or self.last_update is None \
                or ((self.last_update + self.__changeDelta) < datetime.datetime.now()):

            self.data = self.__api.search_station_departures(self.__station_code)
            self.last_update = datetime.datetime.now()

            self.station_name = self.data.location.name
            self.services = self.data.services
            updated_callback(self.__station_code)


class ServiceData:
    def __init__(self, service_uid, date, callback):
        credentials = Credentials()
        api = RttApi(credentials.username, credentials.password)

        self.service_uid = service_uid

        service_info = api.fetch_service_info_datetime(self.service_uid, date)
        self.calling_points = service_info.locations
        callback(self)

