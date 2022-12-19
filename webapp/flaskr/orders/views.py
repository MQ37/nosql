from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
)

from webapp.flaskr.orders import bp
from webapp.flaskr.utils import login_required

from webapp.flaskr.orders.models import Order
from webapp.flaskr.drivers.models import Driver


@bp.route("/")
@login_required
def index_view():

    orders = Order.objects

    return render_template("orders/index.html", orders=orders)


@bp.route("/get")
@login_required
def get_view():
    oid = request.args.get("oid")
    error = None

    if oid:
        try:
            orders = [Order.objects.get(pk=oid)]
            msg = "Success"
        except Exception:
            msg = "Failed to fetch oid"
            error = "invalid oid"
            orders = None

    else:
        orders = list(Order.objects)
        msg = "Success"

    return {
        "msg": msg,
        "error": error,
        "data": orders,
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
            order = Order.objects.get(pk=oid)
            order.delete()
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


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_view():

    if request.method == "POST":
        customer = request.form.get("customer")
        driver = request.form.get("driver")

        # Get driver object
        if driver:
            driver_id = driver.split("(")
            if driver_id:
                driver_id = driver_id[-1].split(")")[0]
                try:
                    driver = Driver.objects.get(pk=driver_id)
                except Exception:
                    driver = None
            else:
                driver = None

        # Validate form and create
        if customer and driver:
            order = Order(customer=customer, driver=driver)
            order.save()
            flash("Order created", "success")
            return redirect(url_for("orders.index_view"))
        else:
            flash("Please fill all fields", "error")

    # Get all drivers for form datalist
    drivers = Driver.objects

    return render_template("orders/add.html", drivers=drivers)

@bp.route("/update/<oid>", methods=["POST", "GET"])
@login_required
def update_view(oid):
    if not oid:
        return redirect(url_for("orders.index_view"))

    try:
        order = Order.objects.get(pk=oid)
    except Exception:
        flash("This order does not exist", "error")
        return redirect(url_for("orders.index_view"))

    # Get all drivers for form datalist
    drivers = Driver.objects

    if request.method == "POST":
        customer = request.form.get("customer")
        driver = request.form.get("driver")

        # Get driver object
        if driver:
            driver_id = driver.split("(")
            if driver_id:
                driver_id = driver_id[-1].split(")")[0]
                try:
                    driver = Driver.objects.get(pk=driver_id)
                except Exception:
                    driver = None
            else:
                driver = None

        if not customer or not driver:
            flash("Please fill all fields", "error")
            return render_template("orders/update.html", customer=customer,
                                                        driver=driver,
                                                        drivers=drivers)


        order.customer = customer
        order.driver = driver
        order.save()

        flash("Order updated", "success")
        return redirect(url_for("orders.index_view"))

    customer = order.customer
    driver = order.driver

    return render_template("orders/update.html", customer=customer,
                                                driver=driver,
                                                drivers=drivers)

