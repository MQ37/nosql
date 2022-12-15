from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for
)

from webapp.flaskr.drivers.models import Driver
from webapp.flaskr.db import db

bp = Blueprint('drivers', __name__,
        template_folder="templates",
        url_prefix='/drivers')

@bp.route("/")
def index_view():
    return render_template("drivers/index.html", drivers=Driver.objects)

@bp.route("/add_driver", methods=["POST", "GET"])
def add_driver():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        age = request.form["age"]

        # Vytvoření a uložení řidiče
        driver = Driver(first_name=first_name, last_name=last_name, age=age)
        driver.save()

        return redirect("/drivers")
    else:
        return render_template("drivers/add-driver.html")