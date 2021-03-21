import yaml

class Config:
    config_file = r"config.yaml"

    def __init__(self):
        config_yaml = self.__credentials()
        self.station = config_yaml.get('station')
        self.platform = config_yaml.get('platform')

        # Display board rendering config
        self.board_width = max(config_yaml.get('board_width'), 48)
        self.additional_services = config_yaml.get('additional_services')

    def __credentials(self):
        with open(self.config_file) as file:
            return yaml.load(file, yaml.FullLoader)