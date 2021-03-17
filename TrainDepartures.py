import datetime

import network.api as api
import config.config as config
import parser.parser as parser
from display.board import Board
import time
import os

# Main body
data = None
lastUpdate = None
changeDelta = datetime.timedelta(minutes=1)
updateThreshold = 60

station = None

columns = 80
board = Board()
#print(parser.all_services(data))

def update_data():
    global data, lastUpdate, updateThreshold, station

    if data is None \
            or lastUpdate is None \
            or ((lastUpdate + changeDelta) < datetime.datetime.now()):
      data = api.fetch_station_info(config.station())
      lastUpdate = datetime.datetime.now()
      station = parser.station_information(data)


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
        columns = 80

def mainloop():
    global station, lastUpdate, data
    while True:
        update_columns()
        update_data()
        clear()
        print_header()

        services = parser.all_services(data)
        board.render(services, station)
        print("%s (%s)" % (station.name, station.code))
        time.sleep(0.1)


mainloop()