from model.station import Station

def station_information(data):
    info = data['location']
    return Station(info['name'], info['crs'])

def all_services(data):
    return __services(data)

def filter_by_platform(data, platform):
    return ""

def __services(data):
    return data['services']