from flask import Blueprint
from ..models import Device, Repo, Device_Model, User
from ..forms import LoginForm, SignupForm
from .. import db

home_bp = Blueprint(
    "home_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)
