class Ticker:
    message = ""        # Visible for testing
    __counter = 0
    __margin = 4

    def __init__(self, config):
        self.__config = config

    def set_message(self, message):
        self.message = "{:>{width}}".format(message, width=(self.__config.board_width + len(message) - self.__margin))
        self.__counter = 0

    def get_and_advance(self):
        out = self.message[self.__counter:(self.__counter + self.__config.board_width - self.__margin)]
        self.__counter += 1
        if self.__counter >= len(self.message):
            self.__counter = 0

        return out