import yaml

class Config:
    def __init__(self):
        config_yaml = self.__credentials()
        self.station = config_yaml.get('station')
        self.platform = config_yaml.get('platform')
        self.board_width = max(config_yaml.get('boardwidth'), 48)

    @staticmethod
    def __credentials():
        with open(r"config.yaml") as file:
            return yaml.load(file, yaml.FullLoader)