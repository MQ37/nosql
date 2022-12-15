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


@bp.route("/get")
def get_view():
    oid = request.args.get("oid")
    error = None

    if oid:
        try:
            drivers = [Driver.objects.get(pk=oid)]
            msg = "Success"
        except Exception:
            msg = "Failed to fetch oid"
            error = "invalid oid"
            drivers = None

    else:
        drivers = list(Driver.objects)
        msg = "Success"

    return {
        "msg": msg,
        "error": error,
        "data": drivers,
    }


@bp.route("/delete", methods=["POST", "DELETE"])
def delete_view():
    if request.method == "POST":
        oid = request.form.get("oid")
    elif request.method == "DELETE":
        oid = request.args.get("oid")

    error = None

    if oid:
        try:
            # TODO: either remove all orders referencing driver or
            # forbid deletion
            driver = Driver.objects.get(pk=oid)
            driver.delete()
            msg = "Success"
        except Exception:
            msg = "Failed to delete oid"
            error = "invalid oid"
    else:
        msg = "OID not specified"
        error = "no oid"

    return {
        "msg": msg,
        "error": error,
    }


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
