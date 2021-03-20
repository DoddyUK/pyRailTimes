# Read credential information from credentials.yaml

import yaml

class Credentials:
    def __init__(self):
        cred_yaml = self.__credentials()
        self.username = cred_yaml.get('user')
        self.password = cred_yaml.get('pass')

    @staticmethod
    def __credentials():
        with open(r"credentials.yaml") as file:
            return yaml.load(file, yaml.FullLoader)