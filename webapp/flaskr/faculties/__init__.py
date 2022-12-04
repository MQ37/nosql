from flask import (
    Blueprint
)

from .models import Faculty


bp = Blueprint('faculties', __name__, url_prefix='/faculties')


@bp.route("/")
def index_view():

    faculties = [f.name for f in Faculty.objects]

    return "Faculties %s" % (faculties)
