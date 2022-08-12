import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

articles = [
    {"author": "AuthorOne", "title": "TitleOne", "publicationYear": 2020},
    {"author": "AuthorTwo", "title": "TitleTwo", "publicationYear": 2021},
    {"author": "AuthorThree", "title": "TitleThree", "publicationYear": 2022},
]


@app.get('/api/v1/articles')
def get_articles():
    return JSONResponse(content={"articles": articles}, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
