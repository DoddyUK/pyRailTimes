import yaml

class Config:
    def __init__(self):
        config_yaml = self.__credentials()
        self.station = config_yaml.get('station')
        self.platform = config_yaml.get('platform')

        # Display board rendering config
        self.board_width = max(config_yaml.get('board_width'), 48)
        self.addional_services = config_yaml.get('additional_services')

    @staticmethod
    def __credentials():
        with open(r"config.yaml") as file:
            return yaml.load(file, yaml.FullLoader)