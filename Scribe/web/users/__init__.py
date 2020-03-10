from flask import Blueprint
from ..models import User
from .. import db

user_bp = Blueprint(
    "user_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/web/users",
)
