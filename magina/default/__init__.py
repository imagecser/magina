from flask import Blueprint

blueprint = Blueprint('default', __name__)

from . import views
