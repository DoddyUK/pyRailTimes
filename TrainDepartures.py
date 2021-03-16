import network.api as api
import config.config as config
import parser.parser as parser

# Main body
data = api.fetch_station_info(config.station())
station = parser.station_information(data)

print("%s (%s)" % (station.name, station.code))

print(parser.all_services(data))