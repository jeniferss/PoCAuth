from connectors.vault_connector import get_credentials

CREDENTIALS = get_credentials(path='credentials', mountpoint='pocauth')

HOST = CREDENTIALS['kongHost']

SERVICE_ID = CREDENTIALS['servicebId']
SERVICE_SECRET = CREDENTIALS['servicebSecret']
