import unittest
import datetime
from unittest.mock import patch
from display.board import Board
from model.calling_point import CallingPoint
from model.station import Station
from model.service import Service

@patch("config.config.Config")
@patch("display.board._Renderer")
class TestBoard(unittest.TestCase):


    def test_draw_box_delegated(self, mock_renderer, mock_config):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)

        # When
        under_test.draw_box()

        # Verify
        renderer.draw_box.assert_called()
        mock_config.return_value.assert_not_called()

    def test_set_station(self, mock_renderer, mock_config):
        # Given
        station = Station("Clapham Junction", "CLJ")
        platform = "7"
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)

        # When
        under_test.set_station(station, platform)

        # Verify
        renderer.update_station_name.assert_called_with(station.name, platform)
        renderer.commit.assert_called()
        mock_config.return_value.assert_not_called()

    def test_update_time(self, mock_renderer, mock_config):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)

        # When
        under_test.update_time()

        # Verify
        renderer.update_time.assert_called()
        renderer.commit.assert_called()
        mock_config.return_value.assert_not_called()

    def test_show_no_services(self, mock_renderer, mock_config):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)

        # When
        under_test.show_no_services()

        # Verify
        renderer.show_no_departures.assert_called()
        renderer.clear_additional_service_row.assert_called()
        renderer.commit.assert_called()
        mock_config.return_value.assert_not_called()


    def test_redraw_with_services(self, mock_renderer, mock_config):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)
        station = Station("Clapham Junction", "CLJ")
        platform = "7"
        services = [
            Service('a1234b', datetime.date(2021, 3, 21), '1140', 'London Waterloo', '1140', '1'),
            Service('a5678c', datetime.date(2021, 3, 21), '1157', 'Basingstoke', '1202', '2')
        ]

        # When
        under_test.set_station(station, platform)
        under_test.update_services(services)
        under_test.redraw()

        # Verify
        renderer.update_station_name.assert_called_with(station.name, platform)
        renderer.update_primary_departure.assert_called_with(services[0])
        renderer.update_additional_service_row.assert_called()
        renderer.commit.assert_called()
        mock_config.return_value.assert_not_called()

    def test_redraw_without_services(self, mock_renderer, mock_config):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)
        station = Station("Clapham Junction", "CLJ")
        platform = "7"
        services = []

        # When
        under_test.set_station(station, platform)
        under_test.update_services(services)
        under_test.redraw()

        # Verify
        renderer.update_station_name.assert_called_with(station.name, platform)
        renderer.show_no_departures.assert_called()
        renderer.clear_additional_service_row.assert_called()
        renderer.commit.assert_called()

        mock_config.return_value.assert_not_called()

    def test_advance_ticker(self, mock_renderer, mock_config):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)
        station = Station("Clapham Junction", "CLJ")
        platform = "7"
        services = [
            Service('a1234b', datetime.date(2021, 3, 21), '1140', 'London Waterloo', '1140', '1'),
            Service('a5678c', datetime.date(2021, 3, 21), '1157', 'Basingstoke', '1202', '2')
        ]

        # When
        under_test.set_station(station, platform)
        under_test.update_services(services)
        under_test.advance_ticker()

        # Verify
        renderer.update_ticker_row.assert_called()
        renderer.commit.assert_called()
        mock_config.return_value.assert_not_called()

    def test_advance_ticker_without_services(self, mock_renderer, mock_config):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)
        station = Station("Clapham Junction", "CLJ")
        platform = "7"
        services = []

        # When
        under_test.set_station(station, platform)
        under_test.update_services(services)
        under_test.advance_ticker()

        # Verify
        renderer.assert_not_called()
        mock_config.return_value.assert_not_called()

    def test_update_calling_points(self, mock_renderer, mock_config):
        # Given
        mock_ticker = unittest.mock.Mock()
        mock_ticker_instance = mock_ticker.return_value

        with patch('display.board.Ticker', mock_ticker_instance):
            under_test = Board(0, 0)

            calling_points = [
                CallingPoint('Woking', 'WOK', '1202', '1202'),
                CallingPoint('Clapham Junction', 'CLJ', '1227', '1227'),
                CallingPoint('Vauxhall', 'VXH', '1235', '1235'),
                CallingPoint('London Waterloo', 'WAT', '1240', '1241'),

            ]

            # When
            under_test.update_service_calling_points(calling_points, 'CLJ')

            # Verify
            mock_renderer.return_value.assert_not_called()
            mock_ticker.return_value.assert_called()
            mock_config.return_value.assert_not_called()

