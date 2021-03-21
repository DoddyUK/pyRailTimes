import datetime
import curses
from config.config import Config

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
            self.board_row(3, "", "Time", "Destination", "Expected")
        ]
        for x in range(5):
            # Blank information board for now
            out.append(self.blank_row())

        out.append(self.bottom_row())

        # draw
        for row, text in enumerate(out):
            self.__window.addstr(row, 0, text)

        self.__window.refresh()

    def update_station_name(self, station_name, platform):
        self.__window.addstr(1, 0, self.__station_row(station_name, platform))
        self.commit()

    def message(self, message):
        return "│ {:^{width}} │".format(message, width=self.__config.board_width - 4)

    def left_message(self, message):
        return "│ {:{width}} │".format(message, width=self.__config.board_width - 4)

    def board_row(self, top, order, time, destination, expected, ):
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
        self.board_row(7, index, service.departureTime, service.destination, expected)

    def blank_row(self):
        return self.message(" ")

    def bottom_row(self):
        return "└─{:─<{leftwidth}}{:^12}{:─<{rightwidth}}─┘".format(
            "─",
            datetime.datetime.now().strftime("%H:%M:%S"),
            "─",
            leftwidth=int((self.__config.board_width - 16) / 2) + (self.__config.board_width % 2),
            rightwidth=int((self.__config.board_width - 16) / 2)
        )

    def commit(self):
        self.__window.refresh()


class _Ticker:
    __message = ""
    __counter = 0

    def __init__(self, config, renderer):
        self.__config = config
        self.__renderer = renderer

    def set_message(self, message):
        self.__message = "{:>{width}}".format(message, width=(self.__config.board_width + len(message)))
        self.__counter = 0

    def render(self):
        out = self.__message[self.__counter:(self.__counter + self.__config.board_width - 4)]
        self.__counter += 1
        if self.__counter >= len(self.__message):
            self.__counter = 0

        self.__renderer.left_message(out)


class _AdditionalServiceFlipper:
    __services = []
    __counter = 0

    __last_change = datetime.datetime.now()
    __change_delta = datetime.timedelta(seconds=5)

    def __init__(self, config, renderer):
        self.__config = config
        self.__renderer = renderer

    def set_services(self, services):
        if len(services) < 2 or self.__config.additional_services < 1:
            self.__services = []
        else:
            self.__services = services[1:self.__config.additional_services]

    def render(self):
        if len(self.__services) < 1:
            self.__renderer.message("*** No additional departures ***")
            return

        if (self.__last_change + self.__change_delta) < datetime.datetime.now():
            self.__last_change = datetime.datetime.now()
            self.__counter = self.__counter + 1
            if self.__counter == self.__config.additional_services or (self.__counter + 1) >= len(self.__services):
                self.__counter = 0

        self.__renderer.service_row(2 + self.__counter, self.__services[1 + self.__counter])


class Board:
    __config = Config()
    __service_info = None

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
        self.__dest_ticker = _Ticker(self.__config, self.__renderer)
        self.__additional_services = _AdditionalServiceFlipper(self.__config, self.__renderer)

    def draw_box(self):
        self.__renderer.draw_box("Loading...", "--")

    def set_station(self, station, platform):
        self.__station = station
        self.__platform = platform
        self.__renderer.update_station_name(station.name, platform)


    def render(self, services):
        self.__additional_services.set_services(services)

        if len(services) == 0:
            self.__renderer.blank_row()
            self.__renderer.message("*** No departures available ***")
            self.__renderer.blank_row()
            self.__renderer.blank_row()
        else:
            self.__renderer.service_row(1, services[0])
            self.__dest_ticker.render()
            self.__renderer.blank_row()
            self.__additional_services.render()

        self.__renderer.bottom_row()

        self.__renderer.commit()

    def update_service_info(self, service_info):
        self.__service_info = service_info

    def update_service_calling_points(self, calling_points):
        stations_togo = []

        for index, value in enumerate(calling_points):
            if value.code == self.__config.station and index + 1 < len(calling_points):
                stations_togo = calling_points[(index + 1):]
                break

        self.__dest_ticker.set_message(_format_calling_points(stations_togo))
