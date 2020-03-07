from flask import Blueprint
from ..models import *
from .. import db

repos_bp = Blueprint('repos_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/web/repos')
