import requests
import settings as cf


class KeycloakConnector:
    def __init__(self):
        self.url = f'{cf.KEYCLOAK_HOST}/realms/{cf.KEYCLOAK_REALM}/protocol/openid-connect/token'

    def generate_user_token(self, body):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'password', 'client_id': cf.KONG_SERVICE_ID, 'client_secret': cf.KONG_SERVICE_SECRET}
        data.update(body)
        response = requests.post(url=self.url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def generate_service_token(self, body):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {"grant_type": "client_credentials"}
        data.update(body)
        response = requests.post(url=self.url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
