from flask import Blueprint
from ..models import *
from .. import db

users_bp = Blueprint('users_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/web/users')
