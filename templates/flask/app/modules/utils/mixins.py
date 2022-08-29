from datetime import datetime

from pytz import timezone

from app.db_connector import db


def current_time():
    return datetime.utcnow().replace(tzinfo=timezone('UTC'))


class TimestampMixin(object):
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=current_time)
    updated = db.Column(db.DateTime(timezone=True), nullable=False, default=current_time, onupdate=current_time)
