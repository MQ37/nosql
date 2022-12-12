from flaskr.db import db


class Driver(db.Document):

    first_name = db.StringField(max_length=60)
    last_name = db.StringField(max_length=60)
    age = db.IntField()

