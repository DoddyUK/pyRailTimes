import datetime
import network.rttapi as api
import parser.parser
from config.config import Config

class Ticker:
    __message = ""
    counter = 0
    config = Config()

    def set_message(self, message):
        self.__message = "{:>{width}}".format(message, width=(self.config.board_width + len(message)))
        self.counter = 0

    def render(self):
        out = self.__message[self.counter:(self.counter + self.config.board_width - 4)]
        self.counter += 1
        if self.counter >= len(self.__message):
            self.counter = 0
        return out


class Board:

    lastChange = datetime.datetime.now()
    changeDelta = datetime.timedelta(seconds=5)

    dest_ticker = Ticker()

    #TODO should be passed in rather than making API calls directly
    serviceInfo = None

    # Counter & limit for additional services
    additionalServices = 3
    serviceCounter = 0

    config = Config()

    def render(self, services, station, platform):
        self.__check_service_info(services, station)

        print(self.__top())
        print(self.__station_row(station, platform))
        print(self.__divider())
        print(self.__header())


        if len(services) == 0:
            print(self.__space_row())
            print(self.__message("*** No departures available ***"))
            print(self.__space_row())
            print(self.__space_row())
        else:
            print(self.__service_row(1, services[0]))
            print(self.__calling_row())
            print(self.__space_row())
            print(self.__additional_service(services))

        print(self.__bottom_row())


    def __check_service_info(self, services, station):
        if len(services) == 0:
            return

        service = services[0]

        if self.serviceInfo is None or service.serviceUid != self.serviceInfo['serviceUid']:
            self.serviceInfo = api.fetch_service_info(service.serviceUid, service.runDate)

            calling_points = parser.parser.calling_points(self.serviceInfo)

            stations_togo = []
            for index, point in enumerate(calling_points):
                if point.code == station.code:
                    stations_togo = calling_points[(index + 1):]

            self.dest_ticker.set_message(self.__format_calling_points(stations_togo))


    def __format_calling_points(self, calling_points):
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


    def __message(self, message):
        return "│{:^{width}}│".format(message, width=self.config.board_width - 2)


    def __top(self):
        return "┌{:─<{width}}┐".format('─', width=self.config.board_width - 2)

    def __divider(self):
        return "├{:─<{width}}┤".format('─', width=self.config.board_width - 2)

    def __header(self):
        return self.__board_row("", "Time", "Destination", "Expected")

    def __board_row(self, order, time, destination, expected, ):
        return "│ {:<3}{:4>}  {:{width}} {:>8} │".format(order, time, destination, expected, width=(self.config.board_width - 22))

    def __station_row(self, station, platform):
        return "│ {name:{width}} │ {platform:>12} │".format(
            name=station.name,
            platform="Platform {}".format(platform),
            width=(self.config.board_width - 19)
        )

    def __space_row(self):
        return self.__message(" ")


    def __service_row(self, index, service):
        expected = "On Time" if (service.expectedTime == service.departureTime) else service.expectedTime
        return self.__board_row(index, service.departureTime, service.destination, expected)

    def __bottom_row(self):
        return "└─{:─<{leftwidth}}{:^12}{:─<{rightwidth}}─┘".format(
            "─",
            datetime.datetime.now().strftime("%H:%M:%S"),
            "─",
            leftwidth=int((self.config.board_width - 16) / 2) + (self.config.board_width % 2),
            rightwidth=int((self.config.board_width - 16) / 2)
        )

    def __calling_row(self):
        return "│ {:{width}} │".format(self.dest_ticker.render(), width=(self.config.board_width - 4))


    def __additional_service(self, services):
        if len(services) <= 1:
            return self.__message("*** No additional departures ***")

        if (self.lastChange + self.changeDelta) < datetime.datetime.now():
            self.lastChange = datetime.datetime.now()
            self.serviceCounter = self.serviceCounter + 1
            if self.serviceCounter == self.additionalServices or (self.serviceCounter + 1) >= len(services):
                self.serviceCounter = 0

        return self.__service_row(2 + self.serviceCounter, services[1 + self.serviceCounter])

    def __stops_list(self):
        return self.__space_row()
