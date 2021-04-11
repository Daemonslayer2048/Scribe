from flask import Blueprint
from .. import db

error_bp = Blueprint(
    "error_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)
