from flaskr.db import db


class Faculty(db.Document):
    name = db.StringField(max_length=60)
