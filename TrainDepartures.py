import datetime

from display.board import Board
from config.config import Config
from data.data import StationData, ServiceData
import time
import os

def _clear():
    os.system("cls" if os.name == "nt" else "clear")


class PyRailTimes:
    __board = Board()
    __services = dict()

    # Default width of the terminal
    __columns = 80

    __config = Config()

    def __init__(self):
        self.__station_data = StationData(self.__config.station)

    def __print_header(self):
        print("{:>{width}}".format("pyRailTimes", width=self.__columns))
        update = "Last update: {}".format(datetime.datetime.strftime(self.__station_data.last_update, "%H:%M:%S"))
        print("{:>{width}}".format(update, width=self.__columns))

    def __update_columns(self):
        try:
            self.__columns, _ = os.get_terminal_size(0)
        except OSError:
            return

    def mainloop(self):
        while True:
            self.__update_columns()
            self.__station_data.check_updates()
            _clear()
            self.__print_header()

            station_code = self.__config.station

            if self.__station_data.station is not None:

                if len(self.__station_data.services) > 0:
                    first_service = self.__station_data.services[0]

                    if station_code not in self.__services:
                        self.__update_service_data(first_service, station_code)

                    elif self.__services[station_code].service_uid != first_service.serviceUid:
                        self.__update_service_data(first_service, station_code)

                self.__board.render(self.__station_data.services, self.__station_data.station, self.__config.platform)

            time.sleep(0.1)

    def __update_service_data(self, service, station_code):
        service_data = ServiceData(service.serviceUid, service.runDate)
        self.__services[station_code] = service_data
        self.__board.update_service_calling_points(service_data.calling_points)

# Entry point
PyRailTimes().mainloop()