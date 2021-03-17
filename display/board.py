import datetime
import network.api as api
import parser.parser

class Board:
    lastChange = datetime.datetime.now()
    changeDelta = datetime.timedelta(seconds=5)

    dest_scroll = ""
    dest_ticker = 0

    serviceInfo = None

    # Counter & limit for additional services
    additionalServices = 3
    serviceCounter = 0

    boxwidth = 70

    def render(self, services):
        self.__check_service_info(services)

        header = "│    Time  Destination %s Exp │" % (" " * (self.boxwidth - 29))
        bottom = "└─ %s ─┘".replace('─', '─' * int((self.boxwidth - 12) / 2)) % datetime.datetime.now().strftime("%H:%M:%S")
        print(self.__top())
        print(header)
        print(self.__space_row())


        if len(services) == 0:
            print(self.__empty_message())
            print(self.__space_row())
            print(self.__space_row())
            print(self.__space_row())
        else:
            print(self.__service_row(1, services[0]))
            print(self.__destination_scroll())
            print(self.__space_row())
            print(self.__additional_service(services))

        print(bottom)


    def __check_service_info(self, services):
        if len(services) == 0:
            return

        service = services[0]

        if self.serviceInfo is None or service.serviceUid != self.serviceInfo['serviceUid']:
            self.serviceInfo = api.fetch_service_info(service.serviceUid, service.runDate)
            self.dest_ticker = 0

            calling_points = parser.parser.calling_points(self.serviceInfo)

            # Concat
            call_str = "Calling at: "
            for point in calling_points:
                call_str += "%s (%s), " % (point.description, point.real_arrival)


            # Add padding at either end for scrolling effect
            self.dest_scroll = (" " * self.boxwidth) + call_str + (" " * self.boxwidth)

    def __empty_message(self):
        return "│%s│" % str.center("*** No departures available ***", self.boxwidth - 2, " ")


    def __top(self):
        return "┌─┐".replace('─', '─' * (self.boxwidth - 2))


    def __space_row(self):
        return "│%s│" % (" " * (self.boxwidth - 2))


    def __service_row(self, index, service):
        left = "%s  %s  %s" % (index, service.departureTime, service.destination)
        expected = "On Time" if (service.expectedTime == service.departureTime) else service.expectedTime
        row = "│ %s%s%s │" % (left, " " * (self.boxwidth - (len(left) + len(expected) + 4)),expected)
        return row


    def __additional_service(self, services):
        if len(services) <= 1:
            return "│%s│" % str.center("*** No additional departures ***", self.boxwidth - 2, " ")

        if (self.lastChange + self.changeDelta) < datetime.datetime.now():
            self.lastChange = datetime.datetime.now()
            self.serviceCounter = self.serviceCounter + 1
            if self.serviceCounter == self.additionalServices or self.serviceCounter >= len(services):
                self.serviceCounter = 0

        return self.__service_row(2 + self.serviceCounter, services[1 + self.serviceCounter])

    def __destination_scroll(self):
        substr = self.dest_scroll[self.dest_ticker:(self.dest_ticker + self.boxwidth - 4)]
        self.dest_ticker += 1

        if (self.dest_ticker + self.boxwidth) >= len(self.dest_scroll):
            self.dest_ticker = 0

        return "│ %s │" % substr


    def __stops_list(self):
        return self.__space_row()


