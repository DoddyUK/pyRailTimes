#!/usr/bin/env python

import datetime
import curses
from curses import wrapper

from display.board import Board
from config.config import Config
from data.data import StationData, ServiceData
import time

class PyRailTimes:
    __board = Board(2, 0)
    __services = dict()

    __config = Config()

    __rows = 0
    __cols = 0


    def __init__(self):
        self.__station_data = StationData(self.__config.station)
        self.__stdscr = curses.initscr()
        self.__update_size()
        curses.noecho()

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __update_size(self):
        self.__rows, self.__cols = self.__stdscr.getmaxyx()

    def __print_header(self):
        title = "pyRailTimes"
        self.__stdscr.addstr(0, max(0, self.__cols - len(title)), title)

        if self.__station_data.last_update is not None:
            update = "Last update: {}".format(datetime.datetime.strftime(self.__station_data.last_update, "%H:%M:%S"))
            self.__stdscr.addstr(1, max(0, self.__cols - len(update)), update)

        self.__stdscr.refresh()

    def __handle_resize(self):
        self.__update_size()
        self.__stdscr.clear()
        curses.resizeterm(self.__rows, self.__cols)
        self.__print_header()
        self.__stdscr.refresh()

    def mainloop(self):
        title = "pyRailTimes"
        self.__stdscr.addstr(0, self.__cols - len(title), title)
        self.__stdscr.refresh()

        while True:

            # Check if screen was re-sized (True or False)
            resize = curses.is_term_resized(self.__rows, self.__cols)
            if resize is not False:
                self.__handle_resize()

            self.__station_data.check_updates(lambda: self.__on_station_update())
            # self.__print_header()

            station_code = self.__config.station

            if self.__station_data.station is not None:

                self.__board.set_station(self.__station_data.station, self.__config.platform)

                if len(self.__station_data.services) > 0:
                    first_service = self.__station_data.services[0]

                    if station_code not in self.__services:
                        self.__update_service_data(first_service)

                    elif self.__services[station_code].service_uid != first_service.serviceUid:
                        self.__update_service_data(first_service)

                self.__board.render(self.__station_data.services)

            time.sleep(0.1)


    def curses_loop(self):
        self.__board.draw_box()

        while True:
            # Check if screen was re-sized (True or False)
            resize = curses.is_term_resized(self.__rows, self.__cols)
            if resize is not False:
                self.__handle_resize()

            self.__station_data.check_updates(lambda: self.__on_station_update())

            time.sleep(0.1)



    def __on_station_update(self):
        self.__print_header()
        self.__board.set_station(self.__station_data.station, self.__config.platform)

        # if len(self.__station_data.services) > 0:
        #     first_service = self.__station_data.services[0]
        #     station_code = self.__config.station
        #
        #     if station_code not in self.__services:
        #         self.__update_service_data(first_service)
        #
        #     elif self.__services[station_code].service_uid != first_service.serviceUid:
        #         self.__update_service_data(first_service)


    def __on_service_update(self, service_data):
        self.__board.update_service_calling_points(service_data.calling_points)

    def __update_service_data(self, service):
        service_data = ServiceData(service.serviceUid, service.runDate, lambda data: self.__on_service_update(data))
        self.__services[self.__config.station] = service_data

# Entry point

if __name__ == '__main__':
    #wrapper(PyRailTimes().mainloop())
    wrapper(PyRailTimes().curses_loop())
