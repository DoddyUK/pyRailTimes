import datetime

import network.rttapi as api
import parser.parser as parser
from display.board import Board
from config.config import Config
import time
import os

# Main body
data = None
lastUpdate = None
changeDelta = datetime.timedelta(minutes=1)
updateThreshold = 60

station = None
board = Board()
services = None

# Default width of the terminal
columns = 80

config = Config()

def update_data():
    global config, data, lastUpdate, updateThreshold, station, board, services

    if data is None \
            or lastUpdate is None \
            or ((lastUpdate + changeDelta) < datetime.datetime.now()):

      data = api.fetch_station_info(config.station)
      lastUpdate = datetime.datetime.now()
      station = parser.station_information(data)
      services = parser.all_services(data)


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    global lastUpdate, columns
    print(str.rjust("Snakes on a Train", columns))
    print(str.rjust("Last update: %s" % datetime.datetime.strftime(lastUpdate, "%H:%M:%S"), columns, " "))

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


mainloop()