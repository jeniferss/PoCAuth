from flask import Flask, request, Response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from mcoloredlogger.functions import setup_logger

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app=app)
ma = Marshmallow(app=app)
migrate = Migrate(app, db)

import logging
logging.getLogger("werkzeug").disabled = True
logger = setup_logger()

@app.after_request
def log_response(response: Response):
    logger.http(f'{request.remote_addr} {request.method} {request.path}', {
                "status": response.status_code})
    return response


def execute_query(query):
    with db.engine.connect() as connection:
        lines = connection.execute(query).fetchall()
        lines = [{key: value for key, value in item.items()} for item in lines]
        return lines
