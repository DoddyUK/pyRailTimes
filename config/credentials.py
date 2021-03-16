# Read credential information from credentials.yaml

import yaml

def username():
        return __credentials().get('user')

def password():
        return __credentials().get('pass')

def __credentials():
    with open(r"credentials.yaml") as file:
        return yaml.load(file, yaml.FullLoader)