from datetime import datetime

import requests
import sys
from requests.auth import HTTPBasicAuth

MENDER_SERVER_URI = 'https://hosted.mender.io/api/management/'
MENDER_SERVER_USER = sys.argv[1]
MENDER_SERVER_PASS = sys.argv[2]


def get_auth_token():
    url = MENDER_SERVER_URI + 'v1/useradm/auth/login'
    response = requests.post(url, auth=HTTPBasicAuth(MENDER_SERVER_USER, MENDER_SERVER_PASS))

    return response.content.decode()


def get_deployments(api_key):
    url = MENDER_SERVER_URI + 'v1/deployments/deployments?page=1'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + str(api_key)
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_devices(api_key):
    url = MENDER_SERVER_URI + 'v2/devauth/devices'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + str(api_key)
    }
    response = requests.get(url, headers=headers)
    return response.json()


def create_deployment(api_key):
    url = MENDER_SERVER_URI + 'deployments/deployments'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + str(api_key)
    }
    date_time = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

    r = requests.post(url, headers=headers)
    body = {
        "name": "inbound-" + date_time,
        "artifact_name": "",
        "devices": [
            "00a0c91e6-7dec-11d0-a765-f81d4faebf6"
        ],
        "retries": 3
    }


if __name__ == "__main__":
    api_key = get_auth_token()
    deployment_list = get_deployments(api_key)
    device_list = get_devices(api_key)
    print(len(device_list))

##r = requests.get('https://hosted.mender.io/api/management/v1/deployments/artifacts', headers = headers)
