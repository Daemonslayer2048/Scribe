from flask import Blueprint
from ..models import *
from .. import db

home_bp = Blueprint('home_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/')
