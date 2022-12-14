from flaskr.db import db


class Driver(db.Document):

    first_name = db.StringField(max_length=60)
    last_name = db.StringField(max_length=60)
    age = db.IntField()

    def __repr__(self):
        return f"Driver (%s) %s %s %s" % (self.id, self.first_name,
                                          self.last_name, self.age)

    def __str__(self):
        return repr(self)
