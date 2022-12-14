from flask import (
    render_template,
    Blueprint,
)

bp = Blueprint('drivers',
               __name__,
               template_folder="templates",
               url_prefix='/drivers')


@bp.route("/")
def index_view():

    return render_template("drivers/index.html")
