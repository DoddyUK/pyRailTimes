import datetime

import network.api as api
import config.config as config
import parser.parser as parser
import time
import os

# Main body
data = None
lastUpdate = None
updateThreshold = 60

station = None

#print(parser.all_services(data))

def update_data():
    global data, lastUpdate, updateThreshold, station

    if data is None or lastUpdate is None or ((lastUpdate + datetime.timedelta(hours=1)) < datetime.datetime.now()):
      data = api.fetch_station_info(config.station())
      lastUpdate = datetime.datetime.now()
      station = parser.station_information(data)


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def mainloop():
    global station, lastUpdate
    while True:
        update_data()
        clear()
        print_header()
        print("%s (%s)" % (station.name, station.code))
        time.sleep(1)

def print_header():
    global lastUpdate
    try:
        columns, rows = os.get_terminal_size(0)
    except OSError:
        columns = 80

    print(str.rjust("Snakes on a Train", columns))
    print(str.rjust("Last update: %s" % datetime.datetime.strftime(lastUpdate, "%H:%M:%S"), columns, " "))

mainloop()