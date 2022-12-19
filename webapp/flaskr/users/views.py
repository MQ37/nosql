from flask import (
    render_template,
    request,
    flash,
    url_for,
    redirect,
    session,
)

from webapp.flaskr.users import bp

from .models import User


@bp.route("/register", methods=["GET", "POST"])
def register_view():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate form and create
        if username and password:
            if len(username) < 4 or len(password) < 4:
                flash("Username and password must have at least 4 chatacters",
                      "error")
            else:
                user = User.create(username=username, password=password)
                flash("User created", "success")
                return redirect(url_for("index_view"))
        else:
            flash("Please fill all fields", "error")

    return render_template("users/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login_view():
    url_next = request.args.get("next")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        url_next = request.form.get("next")

        # Validate form and create
        if username and password:
            user = User.login(username=username, password=password)
            if user:
                session["user"] = str(user.id)
                session["username"] = user.username
                flash("Logged in", "success")
                if url_next:
                    return redirect(url_next)
                else:
                    return redirect(url_for("index_view"))
            else:
                flash("Invalid credentials", "error")

        else:
            flash("Please fill all fields", "error")

    return render_template("users/login.html", url_next=url_next)


@bp.route("/logout")
def logout_view():
    if session.get("user"):
        del session["user"]
        flash("Logged out", "success")
    return redirect(url_for("index_view"))
