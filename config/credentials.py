# Read credential information from credentials.yaml

import yaml

class Credentials:
    credential_file = r"credentials.yaml"
    
    def __init__(self):
        cred_yaml = self.__credentials()
        self.username = cred_yaml.get('user')
        self.password = cred_yaml.get('pass')


    def __credentials(self):
        with open(self.credential_file) as file:
            return yaml.load(file, yaml.FullLoader)