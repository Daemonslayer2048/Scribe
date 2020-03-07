from flask import Blueprint
from ..models import Device_model
from .. import db

device_model_bp = Blueprint('Device_model_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/web/models')
