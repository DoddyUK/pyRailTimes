import datetime
from model.station import Station
from model.service import Service
from model.calling_point import CallingPoint

def station_information(data):
    info = data['location']
    return Station(info['name'], info['crs'])

def all_services(data):
    return __services(data)

def filter_by_platform(data, platform):
    return ""

def calling_points(data):
    out = []

    for location in data['locations']:
        calling_point = CallingPoint(
            location['description'],
            location['gbttBookedArrival'] if 'gbttBookedArrival' in location else location['gbttBookedDeparture'],
            location['realtimeArrival'] if 'realtimeArrival' in location else location['realtimeDeparture']
        )
        out.append(calling_point)

    return out

def __services(data):
    out = []

    for service in data['services']:
        location = service['locationDetail']
        train = Service(
            service['serviceUid'],
            datetime.datetime.strptime(service['runDate'], "%Y-%m-%d").date(),
            location['gbttBookedDeparture'],
            location['destination'][0]['description'],
            location['realtimeDeparture']
        )
        out.append(train)

    return out
