from webapp.flaskr.db import db
from webapp.flaskr.drivers.models import Driver
import datetime


class Order(db.Document):

    customer = db.StringField(max_length=60)
    creation_date = db.DateTimeField()

    driver = db.ReferenceField(Driver)

    # Override save to add default creation_date
    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        return super().save(*args, **kwargs)

    def __repr__(self):
        return "Order (%s) %s %s -> %s" % (self.id, self.customer,
                                           self.creation_date, self.driver)

    def __str__(self):
        return repr(self)
