from flask import Blueprint
from ..models import Device_Model
from .. import db

device_model_bp = Blueprint(
    "device_model_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/web/models",
)
