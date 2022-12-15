from flask import (render_template, Blueprint, request, redirect, url_for)

from webapp.flaskr.drivers.models import Driver
from webapp.flaskr.db import db

bp = Blueprint('drivers',
               __name__,
               template_folder="templates",
               url_prefix='/drivers')

# Register views
import webapp.flaskr.drivers.views
