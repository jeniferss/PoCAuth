from http import client
import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    username: str
    password: str
    client_id: str
    client_secret: str
    grant_type: str

class ServiceRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str


@app.post('/api/v1/token/user')
def gen_token(body: UserRequest):
    try:
        realm = 'pocauth'
        endpoint = f'http://keycloak:8080/realms/{realm}/protocol/openid-connect/token'
        response = requests.post(url=endpoint, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        response.raise_for_status()
        return response.json()

    except Exception as error:
        return {"data": str(error)}, 400


@app.post('/api/v1/token/service')
def gen_client_token(body: ServiceRequest):
    try:
        realm = 'pocauth'
        endpoint = f'http://keycloak:8080/realms/{realm}/protocol/openid-connect/token'
        response = requests.post(url=endpoint, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        response.raise_for_status()
        return response.json()
    except Exception as error:
        return {"data": str(error)}, 400


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000)