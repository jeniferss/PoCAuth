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

class User(BaseModel):
    username: str
    password: str


@app.post('/api/v1/token')
def gen_token(user: User):
    try:
        endpoint = 'http://keycloak:8080/realms/pocauth/protocol/openid-connect/token'
        body = {
            'grant_type': 'password',
            'client_id': 'kong',
            'client_secret': 'WTlikgf93hmucV1AkCEsqntLU18lAepP'
        }
        body.update(user)
        response = requests.post(url=endpoint, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        response.raise_for_status()
        return response.json()

    except Exception as error:
        return {"data": str(error)}, 400


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000)
