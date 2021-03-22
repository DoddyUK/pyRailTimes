#!/usr/bin/env python

import datetime
import curses
import schedule

from display.board import Board
from config.config import Config
from data.data import StationData, ServiceData
import time

class PyRailTimes:
    __services = dict()

    __config = Config()

    __boards = [Board(2, 0), Board(2, __config.board_width + 2)]

    __rows = 0
    __cols = 0

    def __init__(self):
        self.__station_data = StationData(self.__config.station)
        self.__stdscr = curses.initscr()
        self.__update_size()

    def __print_header(self):
        title = "pyRailTimes"
        self.__stdscr.addstr(0, max(0, self.__cols - len(title)), title)

        if self.__station_data.last_update is not None:
            update = "Last update: {}".format(
                datetime.datetime.strftime(self.__station_data.last_update, "%H:%M:%S"))
            self.__stdscr.addstr(1, max(0, self.__cols - len(update)), update)

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
        for board in self.__boards:
            board.update_time()

    def __advance_board_tickers(self):
        for board in self.__boards:
            board.advance_ticker()

    def __advance_board_destinations(self):
        for board in self.__boards:
            board.advance_destinations()

    #
    # Data update handlers
    #
    def __update_station_data(self):
        self.__station_data.check_updates(lambda: self.__on_station_update())

    def __on_station_update(self):
        # Update "last updated" message
        self.__print_header()

        for board in self.__boards:
            board.set_station(self.__station_data.station, self.__config.platform)
            self.__stdscr.refresh()

            if not self.__station_data.services:
                board.show_no_services()

            else:
                first_service = self.__station_data.services[0]
                station_code = self.__config.station

                board.update_services(self.__station_data.services)

                if station_code not in self.__services:
                    self.__update_service_data(first_service)

                elif self.__services[station_code].service_uid != first_service.serviceUid:
                    self.__update_service_data(first_service)


    def __update_service_data(self, service):
        service_data = ServiceData(service.serviceUid, service.runDate, lambda data: self.__on_service_update(data))
        self.__services[self.__config.station] = service_data

    def __on_service_update(self, service_data):
        for board in self.__boards:
            board.update_service_calling_points(service_data.calling_points)

    #
    # Main program loop
    #
    def mainloop(self):
        for board in self.__boards:
            board.draw_box()
            board.update_time()

        self.__station_data.check_updates(lambda: self.__on_station_update())
        self.__setup_schedules()

        while True:
            # Check if screen was re-sized (True or False)
            resize = curses.is_term_resized(self.__rows, self.__cols)
            if resize is True:
                self.__handle_resize()

            schedule.run_pending()
            time.sleep(0.1)

# Entry point
if __name__ == '__main__':
    curses.wrapper(PyRailTimes().mainloop())
