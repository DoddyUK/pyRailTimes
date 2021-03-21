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
    # TODO
    return ""

def calling_points(data):
    out = []

    for location in data['locations']:
        calling_point = CallingPoint(
            location['description'],
            location['crs'],
            location['gbttBookedArrival'] if 'gbttBookedArrival' in location else location['gbttBookedDeparture'],
            location['realtimeArrival'] if 'realtimeArrival' in location else location['realtimeDeparture']
        )
        out.append(calling_point)

    return out

def __services(data):
    out = []

    if data['services'] is not None:
        for service in data['services']:
            location = service['locationDetail']
            # TODO handle multiple destinations where the train splits
            train = Service(
                service['serviceUid'],
                datetime.datetime.strptime(service['runDate'], "%Y-%m-%d").date(),
                location['gbttBookedDeparture'],
                location['destination'][0]['description'],
                location['realtimeDeparture'] if 'realtimeDeparture' in location else "----"  # Replacement buses do not have real time info
            )
            out.append(train)

    return out
