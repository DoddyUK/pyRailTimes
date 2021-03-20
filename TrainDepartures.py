import datetime

import parser.parser as parser
from display.board import Board
from config.config import Config
from network.rttapi import RttApi
import time
import os

# Main body
data = None
lastUpdate = None
changeDelta = datetime.timedelta(minutes=1)
updateThreshold = 60

station = None
service_info = None
board = Board()
services = None

# Default width of the terminal
columns = 80

config = Config()
rtt_api = RttApi()

def update_data():
    global config, data, lastUpdate, updateThreshold, station, board, services

    if data is None \
            or lastUpdate is None \
            or ((lastUpdate + changeDelta) < datetime.datetime.now()):

        data = rtt_api.fetch_station_info(config.station)
        lastUpdate = datetime.datetime.now()
        station = parser.station_information(data)
        services = parser.all_services(data)

        if len(services) > 0:
            __fetch_service_info(services[0])


def __fetch_service_info(service):
    global service_info, board, station

    if service_info is None or service.serviceUid != service_info['serviceUid']:
        service_info = rtt_api.fetch_service_info(service.serviceUid, service.runDate)

        calling_points = parser.calling_points(service_info)

        stations_togo = []
        for index, point in enumerate(calling_points):
            if point.code == station.code:
                stations_togo = calling_points[(index + 1):]

        board.update_service_calling_points(stations_togo)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    global lastUpdate, columns
    print("{:>{width}}".format("pyRailTimes", width=columns))
    update = "Last update: {}".format(datetime.datetime.strftime(lastUpdate, "%H:%M:%S"))
    print("{:>{width}}".format(update, width=columns))

def update_columns():
    global columns
    try:
        columns, _ = os.get_terminal_size(0)
    except OSError:
        return

def mainloop():
    global config, station, lastUpdate, data
    while True:
        update_columns()
        update_data()
        clear()
        print_header()

        if station is not None and services is not None:
            board.render(services, station, config.platform)

        time.sleep(0.1)

# Entry point
mainloop()