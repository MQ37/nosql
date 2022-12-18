from flask_bcrypt import Bcrypt
from functools import wraps
from flask import request, redirect, url_for, session, flash

bcrypt = Bcrypt()


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            flash("You must log in first", "error")
            return redirect(url_for('users.login_view', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
