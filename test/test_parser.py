import unittest
import datetime
import data.parser as parser
from model.service import Service
from model.calling_point import CallingPoint

class TestParser(unittest.TestCase):

    def test_parse_station_information(self):
        station_info = { 'name': "London Waterloo", 'crs': "WAT" }
        data = {'location': station_info }

        actual = parser.station_information(data)
        self.assertEqual("London Waterloo", actual.name)
        self.assertEqual("WAT", actual.code)

    def test_all_services(self):
        service_info = { 'services' :
            [
                {
                    'serviceUid': 'a1234b',
                    'runDate': '2021-03-21',
                    'platform':'1',
                    'locationDetail': {
                        'gbttBookedDeparture': '1140',
                        'destination': [
                            { 'description': 'London Waterloo' }
                        ],
                        'realtimeDeparture': '1140'
                    }
                },
                {
                    'serviceUid': 'a5678c',
                    'runDate': '2021-03-21',
                    'platform':'2',
                    'locationDetail': {
                        'gbttBookedDeparture': '1157',
                        'destination': [
                            {'description': 'Basingstoke'}
                        ],
                        'realtimeDeparture': '1202'
                    }
                },
            ]
        }

        actual = parser.all_services(service_info)

        expected = [
            Service('a1234b', datetime.date(2021, 3, 21), '1140', 'London Waterloo', '1140'),
            Service('a5678c', datetime.date(2021, 3, 21), '1157', 'Basingstoke', '1202')
        ]

        self.assertListEqual(expected, actual)

    def test_filter_by_platform(self):
        # TODO
        return

    def test_missing_departure_time(self):
        service_info = {'services':
            [
                {
                    'serviceUid': 'a1234b',
                    'runDate': '2021-03-21',
                    'platform': '1',
                    'locationDetail': {
                        'gbttBookedDeparture': '1140',
                        'destination': [
                            {'description': 'London Waterloo'}
                        ]
                    }
                }
            ]
        }

        actual = parser.all_services(service_info)

        expected = [
            Service('a1234b', datetime.date(2021, 3, 21), '1140', 'London Waterloo', '----')
        ]

        self.assertListEqual(expected, actual)


    def test_calling_points(self):
        location_info = {
            'locations': [
                {
                    'description': 'Basingstoke',
                    'crs': 'BSK',
                    'gbttBookedArrival': '1204',
                    'realtimeArrival': '1204'
                },
                {
                    'description': 'Woking',
                    'crs': 'WOK',
                    'gbttBookedArrival': '1229',
                    'realtimeArrival': '1231'
                },
                {
                    'description': 'Clapham Junction',
                    'crs': 'CLJ',
                    'gbttBookedArrival': '1258',
                    'realtimeArrival': '1304'
                }
            ]
        }

        expected = [
            CallingPoint('Basingstoke', 'BSK', '1204', '1204'),
            CallingPoint('Woking', 'WOK', '1229', '1231'),
            CallingPoint('Clapham Junction', 'CLJ', '1258', '1304'),
        ]

        actual = parser.calling_points(location_info)
        self.assertEqual(3, len(actual))
        self.assertEqual(expected, actual)

    def test_calling_points_with_arrival_missing(self):
        location_info = {
            'locations': [
                {
                    'description': 'Basingstoke',
                    'crs': 'BSK',
                    'gbttBookedDeparture': '1204',
                    'realtimeDeparture': '1204'
                },
                {
                    'description': 'Woking',
                    'crs': 'WOK',
                    'gbttBookedDeparture': '1229',
                    'realtimeArrival': '1231'
                },
                {
                    'description': 'Clapham Junction',
                    'crs': 'CLJ',
                    'gbttBookedArrival': '1258',
                    'realtimeDeparture': '1304'
                }
            ]
        }

        expected = [
            CallingPoint('Basingstoke', 'BSK', '1204', '1204'),
            CallingPoint('Woking', 'WOK', '1229', '1231'),
            CallingPoint('Clapham Junction', 'CLJ', '1258', '1304'),
        ]

        actual = parser.calling_points(location_info)
        self.assertEqual(3, len(actual))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()