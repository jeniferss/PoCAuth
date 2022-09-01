from connectors.vault_connector import get_credentials

CREDENTIALS = get_credentials(path='credentials', mountpoint='pocauth')

KEYCLOAK_HOST = CREDENTIALS['keycloakHost']
KEYCLOAK_REALM = CREDENTIALS['keycloakRealm']

KONG_SERVICE_ID = CREDENTIALS['kongServiceId']
KONG_SERVICE_SECRET = CREDENTIALS['kongServiceSecret']
