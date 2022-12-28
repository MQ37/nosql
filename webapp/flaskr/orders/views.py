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

from webapp.flaskr.db import graphdb
import neo4j

# City map
ID_CITY = {}
CITY_ID = {}
with graphdb.session() as session:
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
        order = order_fuc()

        # Validate form and create
        if order["customer"] and order["driver"] and order["source"] and order[
                "target"]:
            order = Order(customer=order["customer"],
                          driver=order["driver"],
                          source=order["source"],
                          target=order["target"])
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
        order_dic = order_fuc()

        if not order_dic["customer"] or not order_dic[
                "driver"] or not order_dic["source"] or not order_dic["target"]:
            flash("Please fill all fields", "error")
            return render_template("orders/update.html",
                                   customer=order["customer"],
                                   driver=order["driver"],
                                   drivers=drivers,
                                   cities=cities,
                                   source=source,
                                   target=target)

        order.customer = order_dic["customer"]
        order.driver = order_dic["driver"]
        order.source = order_dic["source"]
        order.target = order_dic["target"]
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


@bp.route("/detail/<oid>")
@login_required
def detail_view(oid):
    if not oid:
        return redirect(url_for("orders.index_view"))

    try:
        order = Order.objects.get(pk=oid)
    except Exception:
        flash("This order does not exist", "error")
        return redirect(url_for("orders.index_view"))

    with graphdb.session() as session:
        cmd = """
        MATCH (source:City), (target:City) WHERE ID(source)=%s AND ID(target)=%s
        CALL gds.shortestPath.dijkstra.stream('highways', {
            sourceNode: source,
            targetNode: target,
            relationshipWeightProperty: 'distance'
        })
        YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
        RETURN
            index,
            gds.util.asNode(sourceNode).name AS sourceNodeName,
            gds.util.asNode(targetNode).name AS targetNodeName,
            totalCost,
            [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
            costs,
            nodes(path) as path
        ORDER BY index
        """ % (order.source, order.target)
        try:
            res = session.run(cmd)
            rec = res.single()
        # Projection does not exist
        except neo4j.exceptions.ClientError:
            res = session.run("""
            CALL gds.graph.project(
            'highways',
            'City',
            'HIGHWAY',
            {
            relationshipProperties: 'distance'
            }
            )
            """)
            res = session.run(cmd)
            rec = res.single()

        total_cost = rec["totalCost"]
        path = []
        for node in rec["path"]:
            path.append(node["name"])
        path = " -> ".join(path)

    source = ID_CITY[order.source]
    target = ID_CITY[order.target]

    return render_template(
        "orders/detail.html",
        order=order,
        customer=order.customer,
        driver=[order.driver.first_name, order.driver.last_name],
        source=source,
        target=target,
        path=path,
        total_cost=total_cost)


def order_fuc():
    order = {}

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

    order['customer'] = customer
    order['driver'] = driver
    order['source'] = source
    order['target'] = target

    return order
