import logging
import os

from hvac import Client
from hvac.exceptions import Unauthorized

credentials = {}


def get_credentials(path: str, mountpoint: str):
    token = os.getenv('VAULTTOKEN')
    server = os.getenv('VAULTSERVER')

    if not token: raise EnvironmentError(f'VTOKEN not declared.')
    if not server: raise EnvironmentError(f'VSERVER not declared.')

    logging.info(f'Consultando path "{path}" no Vault.')
    client = Client(server, token)

    if not client.is_authenticated(): raise Unauthorized('Não autenticado no Vault')

    secrets = client.secrets.kv.v2.read_secret(mount_point=mountpoint, path=path, )['data']['data']
    credentials.update({path: secrets})

    return credentials.get(path)
