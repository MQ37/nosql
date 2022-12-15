from flask import (
    render_template,
    request,
    url_for,
    redirect,
)

from webapp.flaskr.drivers import bp

from webapp.flaskr.drivers.models import Driver


@bp.route("/")
def index_view():
    drivers = Driver.objects

    return render_template("drivers/index.html", drivers=drivers)


@bp.route("/add", methods=["POST", "GET"])
def add_view():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        age = request.form["age"]

        # Vytvoření a uložení řidiče
        driver = Driver(first_name=first_name, last_name=last_name, age=age)
        driver.save()

        return redirect(url_for("drivers.index_view"))
    else:
        return render_template("drivers/add-driver.html")
