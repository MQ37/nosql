from webapp.flaskr.db import db
from webapp.flaskr.utils import bcrypt
import datetime


class User(db.Document):

    username = db.StringField(max_length=30)
    password = db.StringField(max_length=128)
    creation_time = db.DateTimeField()

    # Override save to add default creation_date
    def save(self, *args, **kwargs):
        if not self.creation_time:
            self.creation_time = datetime.datetime.now()
        return super().save(*args, **kwargs)

    @staticmethod
    def create(username, password):
        hashed = bcrypt.generate_password_hash(password)
        u = User(username=username, password=hashed)
        u.save()
        return u

    @staticmethod
    def login(username, password):
        try:
            u = User.objects.get(username=username)
        except Exception:
            return None

        valid = bcrypt.check_password_hash(u.password, password)
        if valid:
            return u
        return None

    def __repr__(self):
        return f"User (%s) %s [%s]" % (self.id, self.username,
                                       self.creation_time)

    def __str__(self):
        return repr(self)
