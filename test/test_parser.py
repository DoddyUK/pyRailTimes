import unittest
import datetime
import data.parser as parser
from model.service import Service

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

        self.assertEqual(2, len(actual))

        expected = [
            Service('a1234b', datetime.date(2021, 3, 21), '1140', 'London Waterloo', '1140'),
            Service('a5678c', datetime.date(2021, 3, 21), '1157', 'Basingstoke', '1202')
        ]

        self.assertListEqual(expected, actual)

    def test_filter_by_platform(self):
        # TODO
        return


if __name__ == '__main__':
    unittest.main()