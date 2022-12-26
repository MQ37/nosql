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

from webapp.flaskr.db import neo4j

# City map
ID_CITY = {}
CITY_ID = {}
with neo4j.session() as session:
    res = session.run("MATCH (n:City) RETURN n")
    for rec in res:
        node = rec.get("n")
        if node:
            CITY_ID[node["name"]] = node.id
            ID_CITY[node.id] = node["name"]


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

    # Convert
    orders = [{
        "_id": {
            "$oid": str(order.pk)
        },
        "creation_time": {
            "$date": str(order.creation_time)
        },
        "customer": order.customer,
        "driver": {
            "$oid": str(order.driver.pk)
        },
        "source": ID_CITY[order.source],
        "target": ID_CITY[order.target],
    } for order in orders]

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
        source = request.form.get("source")
        target = request.form.get("target")

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

        # Get source
        if source:
            source_id = source.split("(")
            if source_id:
                source_id = source_id[-1].split(")")[0]
                if source_id.isdigit():
                    source = source_id
                else:
                    source = None
            else:
                source = None

        # Get target
        if target:
            target_id = target.split("(")
            if target_id:
                target_id = target_id[-1].split(")")[0]
                if target_id.isdigit():
                    target = target_id
                else:
                    target = None
            else:
                target = None

        # Validate form and create
        if customer and driver and source and target:
            order = Order(customer=customer,
                          driver=driver,
                          source=source,
                          target=target)
            order.save()
            flash("Order created", "success")
            return redirect(url_for("orders.index_view"))
        else:
            flash("Please fill all fields", "error")

    # Get all drivers for form datalist
    drivers = Driver.objects

    # Get all cities
    cities = ID_CITY.items()

    return render_template("orders/add.html", drivers=drivers, cities=cities)


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

    # Get all cities
    cities = ID_CITY.items()

    source = "%s (%s)" % (ID_CITY[order.source], order.source)
    target = "%s (%s)" % (ID_CITY[order.target], order.target)

    if request.method == "POST":
        customer = request.form.get("customer")
        driver = request.form.get("driver")
        source = request.form.get("source")
        target = request.form.get("target")

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

        # Get source
        if source:
            source_id = source.split("(")
            if source_id:
                source_id = source_id[-1].split(")")[0]
                if source_id.isdigit():
                    source = source_id
                else:
                    source = None
            else:
                source = None

        # Get target
        if target:
            target_id = target.split("(")
            if target_id:
                target_id = target_id[-1].split(")")[0]
                if target_id.isdigit():
                    target = target_id
                else:
                    target = None
            else:
                target = None

        if not customer or not driver or not source or not target:
            flash("Please fill all fields", "error")
            return render_template("orders/update.html",
                                   customer=customer,
                                   driver=driver,
                                   drivers=drivers,
                                   cities=cities,
                                   source=source,
                                   target=target)

        order.customer = customer
        order.driver = driver
        order.source = source
        order.target = target
        order.save()

        flash("Order updated", "success")
        return redirect(url_for("orders.index_view"))

    customer = order.customer
    driver = order.driver

    return render_template("orders/update.html",
                           customer=customer,
                           driver=driver,
                           drivers=drivers,
                           cities=cities,
                           source=source,
                           target=target)
