from app.db_connector import db, ma
from app.modules.utils.mixins import TimestampMixin

class MyModel(db.Model, TimestampMixin):
    __tablename__ = 'tablename'
    __table_args__ = {'schema': 'schemaname'}

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    myfield = db.Column(db.TEXT, nullable=False)


class MyModelSchema(ma.Schema):
    class Meta:
        fields = ( 'id', 'myfield')


ticket_schema = MyModelSchema
tickets_schema = MyModelSchema(many=True)
