from flask import Blueprint

bp = Blueprint('main', __name__)

from VM_proj_flask.main import routes