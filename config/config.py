import yaml

def station():
        return __credentials().get('station')

def platform():
        return __credentials().get('platform')

def __credentials():
    with open(r"config.yaml") as file:
        return yaml.load(file, yaml.FullLoader)