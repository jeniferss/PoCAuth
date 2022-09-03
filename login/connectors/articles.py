from settings import HOST
import requests
from flask import session


class ArticlesConnector:

    @staticmethod
    def get_articles():
        endpoint = f'{HOST}/api/v1/articles'
        headers = {'Authorization': f'Bearer {session.get("jwt_token")}'}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
