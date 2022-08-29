from hvac import Client
from hvac.exceptions import Unauthorized
import os

credentials = {}


def get_credentials(path):
    if not credentials.get(path):
        env = os.getenv('ENV', 'stg')
        token = os.getenv('VAULT_TOKEN')

        error = []
        if not env: error.append('ENV')
        if not token: error.append('VAULT_TOKEN')

        if error:
            raise EnvironmentError(f'environment variables {error} not declared')

        print(f'Consultando path "{path}" no Vault. Ambiente "{env}"')
        vault_host = os.getenv('VAULT_HOST')
        client = Client(vault_host, token)

        if not client.is_authenticated():
            raise Unauthorized('Não autenticado no Vault')

        key_dict = client.secrets.kv.v2.read_secret(mount_point=env, path=path, )['data']['data']
        credentials.update({path: key_dict})

    return credentials.get(path)