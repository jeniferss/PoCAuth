import os

from hvac import Client
from hvac.exceptions import Unauthorized
import logging

credentials = {}


def get_credentials(path: str):

    token = os.getenv('VTOKEN')
    if not token: raise EnvironmentError(f'VTOKEN not declared.')

    logging.info(f'Consultando path "{path}" no Vault.')
    client = Client('http://vaultserver:8200', token)

    if not client.is_authenticated(): raise Unauthorized('Não autenticado no Vault')

    secrets = client.secrets.kv.v2.read_secret(mount_point='pocauth', path=path, )['data']['data']
    credentials.update({path: secrets})

    return credentials.get(path)
