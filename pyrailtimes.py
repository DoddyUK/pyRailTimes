#!/usr/bin/env python

import curses
import schedule

from display.board import Board
from config.config import Config
from data.data import StationData, ServiceData
import time

class PyRailTimes:
    __services = dict()
    __station_data = dict()
    __boards = dict()

    __config = Config()

    __rows = 0
    __cols = 0

    __board_count = 0

    def __init__(self):
        for config_station in self.__config.stations:
            if config_station.code not in self.__station_data:
                self.__station_data[config_station.code] = StationData(config_station.code)

            if config_station.code not in self.__boards:
                self.__boards[config_station.code] = dict()

            # TODO calculate board positions based on available terminal size
            self.__boards[config_station.code][config_station.platform] = Board((self.__board_count * 10) + 1, 0)
            self.__board_count += 1


        self.__stdscr = curses.initscr()
        self.__update_size()

    def __print_header(self):
        title = "pyRailTimes"
        self.__stdscr.addstr(0, max(0, self.__cols - len(title)), title)

        # if self.__station_data and self.__station_data.values().last_update is not None:
        #     update = "Last update: {}".format(
        #         datetime.datetime.strftime(self.__station_data[0].last_update, "%H:%M:%S"))
        #     self.__stdscr.addstr(1, max(0, self.__cols - len(update)), update)

    #
    # Resize handlers
    #

    def __update_size(self):
        self.__rows, self.__cols = self.__stdscr.getmaxyx()

    def __handle_resize(self):
        self.__update_size()
        self.__stdscr.clear()
        curses.resizeterm(self.__rows, self.__cols)
        self.__stdscr.addstr(0,0,"Rows: {} Cols: {}".format(self.__rows, self.__cols))
        self.__redraw()

    def __redraw(self):
        self.__print_header()
        self.__stdscr.refresh()

        for board in self.__boards:
            board.redraw()

    #
    # Departure Board handlers
    #
    def __setup_schedules(self):
        schedule.every(0.5).seconds.do(self.__update_board_times)
        schedule.every(0.1).seconds.do(self.__advance_board_tickers)
        schedule.every(5).seconds.do(self.__advance_board_destinations)
        schedule.every().minute.do(self.__update_station_data)

    def __update_board_times(self):
        for station_boards in self.__boards.values():
            for board in station_boards.values():
                board.update_time()

    def __advance_board_tickers(self):
        for station_boards in self.__boards.values():
            for board in station_boards.values():
                board.advance_ticker()

    def __advance_board_destinations(self):
        for station_boards in self.__boards.values():
            for board in station_boards.values():
                board.advance_destinations()

    #
    # Data update handlers
    #
    def __update_station_data(self):
        for station_data in self.__station_data.values():
            station_data.check_updates(lambda station_code: self.__on_station_update(station_code))

    def __on_station_update(self, station_code):
        # Update "last updated" message
        self.__print_header()

        data = self.__station_data[station_code]
        boards = self.__boards[station_code]

        for platform, board in boards.items():
            board.set_station(data.station, platform)
            self.__stdscr.refresh()

            if not data.services:
                board.show_no_services()

            else:
                first_service = data.services[0]

                board.update_services(data.services)

                if station_code not in self.__services:
                    self.__update_service_data(first_service, station_code, platform)

                elif self.__services[station_code][platform].service_uid != first_service.serviceUid:
                    self.__update_service_data(first_service, station_code, platform)


    def __update_service_data(self, service, station_code, platform):
        service_data = ServiceData(
            service.serviceUid,
            service.runDate,
            lambda data: self.__on_service_update(data, station_code, platform)

        )
        if station_code not in self.__services:
            self.__services[station_code] = dict
        self.__services[self.__config.stations] = service_data

    def __on_service_update(self, service_data, station_code, platform):
        board = self.__boards[station_code][platform]
        board.update_service_calling_points(service_data.calling_points, station_code)

    #
    # Main program loop
    #
    def mainloop(self):
        for station_boards in self.__boards.values():
            for platform_board in station_boards.values():
                platform_board.draw_box()
                platform_board.update_time()

        for station_data in self.__station_data.values():
            station_data.check_updates(lambda station_code: self.__on_station_update(station_code))

        self.__setup_schedules()

        while True:
            # Check if screen was re-sized (True or False)
            resize = curses.is_term_resized(self.__rows, self.__cols)
            if resize is True:
                self.__handle_resize()

            schedule.run_pending()
            time.sleep(0.1)

class ConfigTest:
    __config = Config()

    def print_stations(self):
        for station in self.__config.stations:
            print(station)

# Entry point
if __name__ == '__main__':
    # ConfigTest().print_stations()
    curses.wrapper(PyRailTimes().mainloop())
