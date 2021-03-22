import datetime
from model.station import Station
from model.service import Service
from model.calling_point import CallingPoint

def station_information(data):
    info = data['location']
    return Station(info['name'], info['crs'])

def all_services(data):
    return __services(data)

def calling_points(data):
    out = []

    for location in data['locations']:
        calling_point = CallingPoint(
            location['description'],
            location['crs'],
            __optional(location, 'gbttBookedArrival', __optional(location, 'gbttBookedDeparture', "Unknown")),
            __optional(location, 'realtimeArrival', __optional(location, 'realtimeDeparture', "Unknown"))
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
                __optional(location, 'realtimeDeparture', "----"),
                __optional(location, 'platform', "")
            )
            out.append(train)

    return out

def __optional(data, key, default):
    return data[key] if key in data else default