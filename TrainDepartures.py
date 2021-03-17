import network.api as api
import config.config as config
import parser.parser as parser
import time
from os import system, name

# Main body
data = None
lastUpdate = None
updateThreshold = 60

station = None

#print(parser.all_services(data))

def update_data():
    global data, lastUpdate, updateThreshold, station

    if data is None or lastUpdate is None or (lastUpdate + updateThreshold) < time.time():
      data = api.fetch_station_info(config.station())
      lastUpdate = time.time()
      station = parser.station_information(data)


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def mainloop():
    global station, lastUpdate
    while True:
        update_data()
        clear()
        print("%s (%s)" % (station.name, station.code))
        print("last update: %s", lastUpdate)
        time.sleep(1)

mainloop()