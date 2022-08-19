import os

import requests
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

import settings as cf

app = FastAPI()

origins = [
    "http://localhost:8000",
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

@app.get('/api/v1/articles')
def get_articles():
    try:
        endpoint = f'{cf.HOST}/api/v1/articles'
        token = os.getenv('TOKEN')
        response = requests.get(url=endpoint, headers={'Authorization': token})
        response.raise_for_status()
        return JSONResponse(content=response.json(), status_code=200)
    except Exception as error:
        return JSONResponse(content={"error": str(error)}, status_code=400)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
