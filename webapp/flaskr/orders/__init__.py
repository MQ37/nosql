from flask import (
    render_template,
    Blueprint,
)


bp = Blueprint('orders', __name__,
        template_folder="templates",
        url_prefix='/orders')


@bp.route("/")
def index_view():

    return render_template("orders/index.html")
