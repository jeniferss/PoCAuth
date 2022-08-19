import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.keycloak_connector import KeycloakConnector

app = FastAPI()
keycloak_connector = KeycloakConnector()

origins = [
    "http://localhost:3000",
    "http://server.one:3001",
    "http://server.two:3002",
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


class ServiceRequest(BaseModel):
    client_id: str
    client_secret: str


@app.post('/api/v1/token/user')
def gen_token(user: UserRequest):
    try:
        content = keycloak_connector.generate_user_token(user)
        return JSONResponse(content=content, status_code=200)
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=400)


@app.post('/api/v1/token/service')
def gen_client_token(service: ServiceRequest):
    try:
        content = keycloak_connector.generate_service_token(service)
        return JSONResponse(content=content, status_code=200)
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=400)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000)
