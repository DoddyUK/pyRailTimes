import unittest
from unittest.mock import patch
from display.board import Board
from model.station import Station

class TestBoard(unittest.TestCase):

    @patch("display.board._Renderer")
    def test_draw_box_delegated(self, mock_renderer):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)

        # When
        under_test.draw_box()

        # Verify
        renderer.draw_box.assert_called()

    @patch("display.board._Renderer")
    def test_set_station(self, mock_renderer):
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

    @patch("display.board._Renderer")
    def test_update_time(self, mock_renderer):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)

        # When
        under_test.update_time()

        # Verify
        renderer.update_time.assert_called()
        renderer.commit.assert_called()

    @patch("display.board._Renderer")
    def test_show_no_services(self, mock_renderer):
        # Given
        renderer = mock_renderer.return_value
        under_test = Board(0, 0)

        # When
        under_test.show_no_services()

        # Verify
        renderer.show_no_departures.assert_called()
        renderer.clear_additional_service_row.assert_called()
        renderer.commit.assert_called()
