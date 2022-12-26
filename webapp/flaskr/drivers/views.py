from flask import (render_template, request, url_for, redirect, flash)

from webapp.flaskr.drivers import bp
from webapp.flaskr.utils import login_required

from webapp.flaskr.orders.models import Order
from webapp.flaskr.drivers.models import Driver


@bp.route("/")
@login_required
def index_view():
    drivers = Driver.objects

    return render_template("drivers/index.html", drivers=drivers)


@bp.route("/get")
@login_required
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
@login_required
def delete_view():
    if request.method == "POST":
        oid = request.form.get("oid")
    elif request.method == "DELETE":
        oid = request.args.get("oid")

    error = None

    if oid:
        try:
            driver = Driver.objects.get(pk=oid)
            orders = Order.objects(driver=driver).all()
            if orders:
                msg = "Cannot delete this driver, delete related orders first"
                error = "remove related orders"
            else:
                driver.delete()
                msg = "Success"
        except Exception as ex:
            msg = "Failed to delete oid"
            error = "operation failed"
    else:
        msg = "OID not specified"
        error = "no oid"

    return {
        "msg": msg,
        "error": error,
    }


@bp.route("/add", methods=["POST", "GET"])
@login_required
def add_view():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        age = request.form["age"]

        # Vytvoření a uložení řidiče
        driver = Driver(first_name=first_name, last_name=last_name, age=age)
        driver.save()

        flash("The driver has been successfully added to the database!",
              "success")
        return redirect(url_for("drivers.index_view"))
    else:
        return render_template("drivers/add-driver.html")


@bp.route("/update/<oid>", methods=["POST", "GET"])
@login_required
def update_view(oid):
    if not oid:
        return redirect(url_for("drivers.index_view"))

    try:
        driver = Driver.objects.get(pk=oid)
    except Exception:
        flash("This driver does not exist", "error")
        return redirect(url_for("drivers.index_view"))

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")

        if not first_name or not last_name or not age:
            flash("Please fill all fields", "error")
            return render_template("drivers/update.html",
                                   first_name=first_name,
                                   last_name=last_name,
                                   age=age)

        driver.first_name = first_name
        driver.last_name = last_name
        driver.age = age
        driver.save()

        flash("Driver updated", "success")
        return redirect(url_for("drivers.index_view"))

    first_name = driver.first_name
    last_name = driver.last_name
    age = driver.age
    return render_template("drivers/update.html",
                           first_name=first_name,
                           last_name=last_name,
                           age=age)
