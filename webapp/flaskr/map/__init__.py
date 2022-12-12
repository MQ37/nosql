from flask import (
    render_template,
    Blueprint,
)

bp = Blueprint('map', __name__,
        template_folder="templates",
        url_prefix='/map')

@bp.route("/")
def index_view():

    return render_template("map/index.html")

