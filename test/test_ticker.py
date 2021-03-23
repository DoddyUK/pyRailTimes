import unittest
from display.ticker import Ticker


class _MockConfig:
    board_width = 40


class TestParser(unittest.TestCase):
    def setUp(self):
        self.__config = _MockConfig()
        self.under_test = Ticker(self.__config)

    def test_spacing_added(self):
        # Given
        input_msg = "Example Message"
        expected = "{}{}".format(" " * (self.__config.board_width - 4), input_msg)

        # When
        self.under_test.set_message(input_msg)

        self.assertEqual(expected, self.under_test.message)

    def test_ticker_advancing(self):

        # When
        self.under_test.set_message("Example Message")

        # First advancement
        expected = "{}".format(" " * (self.__config.board_width - 4))
        self.assertEqual(expected, self.under_test.get_and_advance())

        # Second advancement
        expected = "{}E".format(" " * (self.__config.board_width - 5))
        self.assertEqual(expected, self.under_test.get_and_advance())

        # Third advancement
        expected = "{}Ex".format(" " * (self.__config.board_width - 6))
        self.assertEqual(expected, self.under_test.get_and_advance())

    def test_ticker_reset(self):
        # Given
        input_msg = "test"
        self.__config.board_width = 12

        #When
        self.under_test.set_message(input_msg)
        for i in range(self.__config.board_width - 2):
            self.under_test.get_and_advance()

        #verify
        self.assertEqual("st", self.under_test.get_and_advance())
        self.assertEqual("t", self.under_test.get_and_advance())
        self.assertEqual("{}".format(" " * 8), self.under_test.get_and_advance())