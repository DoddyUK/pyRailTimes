from model.station import Station
from model.service import Service

def station_information(data):
    info = data['location']
    return Station(info['name'], info['crs'])

def all_services(data):
    return __services(data)

def filter_by_platform(data, platform):
    return ""

def __services(data):
    out = []

    for service in data['services']:
        location = service['locationDetail']
        train = Service(
            location['gbttBookedDeparture'],
            location['destination'][0]['description'],
            location['realtimeDeparture']
        )
        out.append(train)

    return out
