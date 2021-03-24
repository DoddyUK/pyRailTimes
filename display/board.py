import datetime
import curses
from config.config import Config
from display.ticker import Ticker

def _format_calling_points(calling_points):
    # Concat
    call_str = "Calling at: "

    if len(calling_points) == 1:
        call_str += "{} ({}) only.".format(calling_points[0].description, calling_points[0].real_arrival)
    else :
        for point in calling_points:
            if point == calling_points[-1]:
                call_str += "and {} ({})".format(point.description, point.real_arrival)
            else:
                call_str += "{} ({}), ".format(point.description, point.real_arrival)

    return call_str


class _Renderer:
    def __init__(self, config, top, left):
        self.__config = config
        self.__stdscr = curses.initscr()
        self.__window = curses.newwin(50, config.board_width, top, left)

    def draw_box(self, station_name, platform):
        # build buffer
        # header
        out = [
            self.__top(),
            self.__station_row(station_name, platform),
            self.__divider(),
            self.board_row("", "Time", "Destination", "Expected")
        ]
        for x in range(4):
            # Blank information board for now
            out.append(self.blank_row())

        # draw
        for row, text in enumerate(out):
            self.__window.addstr(row, 0, text)

        self.update_time()
        self.__window.refresh()

    def update_station_name(self, station_name, platform):
        self.__window.addstr(1, 0, self.__station_row(station_name, platform))

    def show_no_departures(self):
        self.__window.addstr(4, 0, self.blank_row())
        self.__window.addstr(5, 0, self.message("*** No departures available ***"))
        self.__window.addstr(6, 0, self.blank_row())
        self.__window.addstr(7, 0, self.blank_row())

    def update_primary_departure(self, service):
        self.__window.addstr(4, 0, self.board_row(1, service.departureTime, service.destination, service.expectedTime))

    def update_ticker_row(self, message):
        self.__window.addstr(5, 0, self.left_message(message))

    def message(self, message):
        return "│ {:^{width}} │".format(message, width=self.__config.board_width - 4)

    def left_message(self, message):
        return "│ {:{width}} │".format(message, width=self.__config.board_width - 4)

    def board_row(self, order, time, destination, expected):
        return "│ {:<3}{:4>}  {:{width}} {:>8} │".format(
            order,
            time,
            destination,
            expected,
            width=(self.__config.board_width - 22)
        )


    def __top(self):
        return "┌{:─<{width}}┐".format('─', width=self.__config.board_width - 2)

    def __divider(self):
        return "├{:─<{width}}┤".format('─', width=self.__config.board_width - 2)

    def __station_row(self, station_name, platform):
        return "│ {name:{width}} │ {platform:>12} │".format(
                name=station_name,
                platform="Platform {}".format(platform),
                width=(self.__config.board_width - 19)
            )


    def service_row(self, index, service):
        expected = "On Time" if (service.expectedTime == service.departureTime) else service.expectedTime
        return self.board_row(index, service.departureTime, service.destination, expected)

    def blank_row(self):
        return self.message(" ")

    def update_time(self):
        time_row = "└─{:─<{leftwidth}}{:^12}{:─<{rightwidth}}─┘".format(
            "─",
            datetime.datetime.now().strftime("%H:%M:%S"),
            "─",
            leftwidth=int((self.__config.board_width - 16) / 2) + (self.__config.board_width % 2),
            rightwidth=int((self.__config.board_width - 16) / 2)
        )
        self.__window.addstr(8, 0, time_row)

    def update_additional_service_row(self, index, service):
        if not service:
            message = self.message("*** No additional departures ***")
        else:
            message = self.service_row(index, service)

        self.__window.addstr(7, 0, message)

    def clear_additional_service_row(self):
        self.__window.addstr(7, 0, self.blank_row())


    def commit(self):
        self.__window.refresh()


class AdditionalServiceFlipper:
    __services = []
    __counter = 0

    def __init__(self, config):
        self.__config = config

    def set_services(self, services):
        if len(services) < 2 or self.__config.additional_services < 1:
            self.__services = []
        else:
            self.__services = services[1:self.__config.additional_services]

    def get_and_advance(self):
        pair = self.get()
        self.__advance_counter()
        return pair

    def get(self):
        if not self.__services:
            return -1, None
        else:
            return 2 + self.__counter, self.__services[self.__counter]

    def __advance_counter(self):
        self.__counter += 1
        if self.__counter == self.__config.additional_services or (self.__counter + 1) >= len(self.__services):
            self.__counter = 0


class Board:
    __config = Config()
    __services = None

    __station = ""
    __platform = ""

    # TODO Handle cancelled services:
    # "cancelReasonCode": "TG",
    #  "cancelReasonShortText": "issue with train crew",
    #  "cancelReasonLongText": "an issue with the train crew",
    #  "displayAs": "CANCELLED_CALL"

    def __init__(self, top, left):
        self.__top = top
        self.__left = left
        self.__renderer = _Renderer(self.__config, top, left)
        self.__dest_ticker = Ticker(self.__config)
        self.__additional_services = AdditionalServiceFlipper(self.__config)

    def draw_box(self):
        self.__renderer.draw_box("Loading...", "--")

    def set_station(self, station, platform):
        self.__station = station
        self.__platform = platform
        self.__renderer.update_station_name(station.name, platform)
        self.__renderer.commit()

    def update_services(self, services, redraw=False):
        # Only update the board if we have new info
        if services != self.__services or redraw is True:
            self.__services = services

            if not services:
                self.__renderer.show_no_departures()
                self.__renderer.clear_additional_service_row()
            else:
                self.__renderer.update_primary_departure(self.__services[0])
                self.__additional_services.set_services(services)
                index, service = self.__additional_services.get() if redraw is True else self.__additional_services.get_and_advance()
                self.__renderer.update_additional_service_row(index, service)

            self.__renderer.commit()

    def update_service_calling_points(self, calling_points, station_code):
        stations_togo = []

        for index, value in enumerate(calling_points):
            if value.code == station_code and index + 1 < len(calling_points):
                stations_togo = calling_points[(index + 1):]
                break

        self.__dest_ticker.set_message(_format_calling_points(stations_togo))

    def update_time(self):
        self.__renderer.update_time()
        self.__renderer.commit()

    def show_no_services(self):
        self.update_services([])

    def advance_ticker(self):
        if self.__services:
            self.__renderer.update_ticker_row(self.__dest_ticker.get_and_advance())
            self.__renderer.commit()

    def advance_destinations(self):
        if self.__services:
            index, service = self.__additional_services.get_and_advance()
            self.__renderer.update_additional_service_row(index, service)
            self.__renderer.commit()

        else:
            self.__renderer.clear_additional_service_row()


    def redraw(self):
        self.draw_box()

        if self.__station != "" and self.__platform != "":
            self.__renderer.update_station_name(self.__station.name, self.__platform)
            self.update_services(self.__services if self.__services else [], True)
