import requests
from requests.auth import HTTPBasicAuth
import config.credentials as credentials

urlBase = "https://api.rtt.io/api/v1"

def test_call():
    url = "%s/json/search/SOU" % urlBase
    auth = HTTPBasicAuth(credentials.username(), credentials.password())

    print(url)

    response = requests.get(url, auth=auth)

    if response.ok:
        return response.json()
    else:
        return "Request failed"