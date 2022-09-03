from connectors.vault import get_credentials

CREDENTIALS = get_credentials(path='credentials', mountpoint='pocauth')

HOST = CREDENTIALS['kongHost']
