import datetime
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
    def __init__(self, config):
        self.__config = config

    def message(self, message):
        print("│ {:^{width}} │".format(message, width=self.__config.board_width - 4))

    def left_message(self, message):
        print("│ {:{width}} │".format(message, width=self.__config.board_width - 4))

    def board_row(self, order, time, destination, expected, ):
        print(
            "│ {:<3}{:4>}  {:{width}} {:>8} │".format(
                order,
                time,
                destination,
                expected,
                width=(self.__config.board_width - 22)
            )
        )

    def __top(self):
        print("┌{:─<{width}}┐".format('─', width=self.__config.board_width - 2))

    def __divider(self):
        print("├{:─<{width}}┤".format('─', width=self.__config.board_width - 2))

    def __station_row(self, station, platform):
        print(
            "│ {name:{width}} │ {platform:>12} │".format(
                name=station.name,
                platform="Platform {}".format(platform),
                width=(self.__config.board_width - 19)
            )
        )

    def header(self, station, platform):
        self.__top()
        self.__station_row(station, platform)
        self.__divider()
        self.board_row("", "Time", "Destination", "Expected")

    def service_row(self, index, service):
        expected = "On Time" if (service.expectedTime == service.departureTime) else service.expectedTime
        self.board_row(index, service.departureTime, service.destination, expected)

    def blank_row(self):
        self.message(" ")

    def bottom_row(self):
        print(
            "└─{:─<{leftwidth}}{:^12}{:─<{rightwidth}}─┘".format(
                "─",
                datetime.datetime.now().strftime("%H:%M:%S"),
                "─",
                leftwidth=int((self.__config.board_width - 16) / 2) + (self.__config.board_width % 2),
                rightwidth=int((self.__config.board_width - 16) / 2)
            )
        )


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
        if len(services) < 2 or self.__config.addional_services < 1:
            self.__services = []
        else:
            self.__services = services[1:self.__config.addional_services]

    def render(self):
        if len(self.__services) < 1:
            self.__renderer.message("*** No additional departures ***")
            return

        if (self.__last_change + self.__change_delta) < datetime.datetime.now():
            self.__last_change = datetime.datetime.now()
            self.__counter = self.__counter + 1
            if self.__counter == self.__config.addional_services or (self.__counter + 1) >= len(self.__services):
                self.__counter = 0

        self.__renderer.service_row(2 + self.__counter, self.__services[1 + self.__counter])


class Board:
    __config = Config()
    __renderer = _Renderer(__config)
    __dest_ticker = _Ticker(__config, __renderer)
    __additional_services = _AdditionalServiceFlipper(__config, __renderer)
    __service_info = None

    # TODO Handle cancelled services:
    # "cancelReasonCode": "TG",
    #  "cancelReasonShortText": "issue with train crew",
    #  "cancelReasonLongText": "an issue with the train crew",
    #  "displayAs": "CANCELLED_CALL"

    def render(self, services, station, platform):
        self.__additional_services.set_services(services)
        self.__renderer.header(station, platform)

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

    def update_service_info(self, service_info):
        self.__service_info = service_info

    def update_service_calling_points(self, calling_points):
        stations_togo = []

        for index, value in enumerate(calling_points):
            if value.code == self.__config.station and index + 1 < len(calling_points):
                stations_togo = calling_points[(index + 1):]
                break

        self.__dest_ticker.set_message(_format_calling_points(stations_togo))
