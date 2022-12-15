from flask import (
    render_template,
    request,
    flash,
)

from webapp.flaskr.orders import bp

from webapp.flaskr.orders.models import Order
from webapp.flaskr.drivers.models import Driver


@bp.route("/")
def index_view():

    return render_template("orders/index.html")


@bp.route("/add", methods=["GET", "POST"])
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
            print("Order created", "success")
        else:
            flash("Please fill all fields", "error")
            print("Please fill all fields", "error")

    # Get all drivers for form datalist
    drivers = Driver.objects

    return render_template("orders/add.html", drivers=drivers)
