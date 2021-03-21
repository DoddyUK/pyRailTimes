import unittest
import data.parser as parser

class TestParser(unittest.TestCase):

    def test_parse_station_information(self):
        station_info = { 'name': "London Waterloo", 'crs': "WAT" }
        data = {'location': station_info }

        actual = parser.station_information(data)
        self.assertEqual("London Waterloo", actual.name)
        self.assertEqual("WAT", actual.code)


if __name__ == '__main__':
    unittest.main()