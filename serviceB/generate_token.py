import jwt
import requests
import os

try:
    consumer = os.getenv('CONSUMER', 'CONSUMER')
    endpoint = f'http://kong:8001/consumers/{consumer}/jwt'
    response = requests.get(url=endpoint).json()
    key = response['data'][0]['key']
    secret = response['data'][0]['secret']
    
    TOKEN = jwt.encode(payload={'iss': key}, key=secret, algorithm='HS256', headers={"typ": "JWT", "alg": "HS256"})
    TOKEN = f'Bearer {TOKEN}'
    os.environ['TOKEN'] = TOKEN

except Exception as error:
    print(f'Wrong consumer id. Error: {error}')

os.system('uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 7000')
