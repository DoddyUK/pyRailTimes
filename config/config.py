import yaml
from model.station import ConfigStation

class Config:
    config_file = r"config.yaml"

    def __init__(self):
        config_yaml = self.__load()
        print(config_yaml)
        print(config_yaml.get('stations'))
        self.stations = map(self.__to_config_station, config_yaml.get('stations'))

        # Display board rendering config
        self.board_width = max(config_yaml.get('board_width'), 48)
        self.additional_services = config_yaml.get('additional_services')

    def __to_config_station(self, yaml_item):
        return ConfigStation(
            yaml_item.get('code'),
            yaml_item.get('platform')
        )

    def __load(self):
        with open(self.config_file) as file:
            return yaml.load(file, yaml.FullLoader)