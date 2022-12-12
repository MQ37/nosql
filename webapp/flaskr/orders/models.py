from flaskr.db import db
from flaskr.drivers.models import Driver


class Order(db.Document):

    customer = db.StringField(max_length=60)
    driver = db.ReferenceField(Driver)
