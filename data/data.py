import datetime
import data.parser as parser
from network.api import RttApi

# TODO these data objects should have callback methods to signal when an update has occurred

class StationData:
    data = None
    last_update = None
    station = None
    services = None
    __changeDelta = datetime.timedelta(minutes=1)

    __api = RttApi()

    def __init__(self, station_code):
        self.__station_code = station_code

    def check_updates(self, updated_callback):
        if self.data is None \
                or self.last_update is None \
                or ((self.last_update + self.__changeDelta) < datetime.datetime.now()):

            self.data = self.__api.fetch_station_info(self.__station_code)
            self.last_update = datetime.datetime.now()

            self.station = parser.station_information(self.data)
            self.services = parser.all_services(self.data)
            updated_callback(self.__station_code)


class ServiceData:
    __api = RttApi()

    def __init__(self, service_uid, date, callback):
        self.service_uid = service_uid
        self.__data = self.__api.fetch_service_info(self.service_uid, date)
        self.calling_points = parser.calling_points(self.__data)
        callback(self)

