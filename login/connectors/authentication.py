from settings import HOST
import requests


class AuthConnector:

    @staticmethod
    def user_login(body: dict):
        endpoint = f'{HOST}/api/v1/token/user'
        response = requests.post(endpoint, json=body, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()
