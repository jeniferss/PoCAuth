import os
import logging
import requests

import settings as cf

try:
    body = {"client_id": cf.SERVICE_ID, "client_secret": cf.SERVICE_SECRET}
    url = f'{cf.HOST}/api/v1/token/service'
    response = requests.post(url=url, json=body)
    response.raise_for_status()
    response = response.json()
    ACCESS = response['access_token']
    os.environ['TOKEN'] = f'Bearer {ACCESS}'

except Exception as error:
    logging.error(f'Error while generating token. Error: {str(error)}')

os.system('uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 7000')
