from flask import Blueprint
from ..models import Group
from .. import db

device_bp = Blueprint('device_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/web/devices')
