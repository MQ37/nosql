from flask import Blueprint

bp = Blueprint('orders',
               __name__,
               template_folder="templates",
               url_prefix='/orders')

# Register views
from . import views
