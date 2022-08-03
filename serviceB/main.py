import os

import requests
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/api/v1/callServiceA')
def get_articles():
    try:
        endpoint = 'http://kong:8000/api/v1/articles'
        token = os.getenv('TOKEN', None)
        response = requests.get(url=endpoint, headers={'Authorization': token})
        response.raise_for_status()
        return {"data": response.json()}
    except Exception as error:
        return {"data": str(error)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
