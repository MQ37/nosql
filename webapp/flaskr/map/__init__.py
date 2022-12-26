from flask import Blueprint

bp = Blueprint('map', __name__, template_folder="templates", url_prefix='/map')

# Register views
from . import views
