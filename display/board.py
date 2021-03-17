import datetime

class Board:
    boxwidth = 44

    def render(self, services):
        header = "│    Time  Destination %s Exp │" % (" " * (self.boxwidth - 29))
        bottom = "└─ %s ─┘".replace('─', '─' * int((self.boxwidth - 12) / 2)) % datetime.datetime.now().strftime("%H:%M:%S")
        print(self.__top())
        print(header)
        print(self.__space_row())
        print(self.__service_row(1, services[0]))
        print(bottom)

    def __top(self):
        return "┌─┐".replace('─', '─' * (self.boxwidth - 2))

    def __space_row(self):
        return "│%s│" % (" " * (self.boxwidth - 2))

    def __service_row(self, index, service):
        left = "%s  %s  %s" % (index, service.departureTime, service.destination)
        expected = "On Time" if (service.expectedTime == service.departureTime) else service.expectedTime
        row = "│ %s%s%s │" % (left, " " * (self.boxwidth - (len(left) + len(expected) + 4)),expected)
        return row