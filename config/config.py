import yaml
from model.station import ConfigStation


def _to_config_station(yaml_item):
    return ConfigStation(
        yaml_item.get('code'),
        yaml_item.get('platform')
    )


class Config:
    config_file = r"config.yaml"

    def __init__(self):
        config_yaml = self.__load()
        self.stations = map(_to_config_station, config_yaml.get('stations'))

        # Display board rendering config
        self.board_width = max(config_yaml.get('board_width'), 48)
        self.additional_services = config_yaml.get('additional_services')

    def __load(self):
        with open(self.config_file) as file:
            return yaml.load(file, yaml.FullLoader)