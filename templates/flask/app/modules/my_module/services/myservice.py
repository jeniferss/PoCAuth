from flask import Request, Response
from flask import jsonify


def hello(request: Request) -> Response:
    return jsonify({"message": "Hello World!"})
