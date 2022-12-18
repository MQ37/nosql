from flask import Blueprint

bp = Blueprint('drivers',
               __name__,
               template_folder="templates",
               url_prefix='/drivers')

# Register views
from . import views
