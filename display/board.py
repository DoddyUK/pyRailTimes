import datetime

class Board:
    lastChange = datetime.datetime.now()
    changeDelta = datetime.timedelta(seconds=5)

    # Counter & limit for additional services
    additionalServices = 3
    serviceCounter = 0

    boxwidth = 50

    def render(self, services):
        header = "│    Time  Destination %s Exp │" % (" " * (self.boxwidth - 29))
        bottom = "└─ %s ─┘".replace('─', '─' * int((self.boxwidth - 12) / 2)) % datetime.datetime.now().strftime("%H:%M:%S")
        print(self.__top())
        print(header)
        print(self.__space_row())

        if len(services) == 0:
            print(self.__empty_message())
        else:
            print(self.__service_row(1, services[0]))
            print(self.__space_row()) # TODO scrolling stops list
            print(self.__additional_service(services))

        print(bottom)

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


