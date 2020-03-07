from flask import Blueprint
from ..models import Device, Repo, Device_model
from ..forms import LoginForm
from .. import db

home_bp = Blueprint('home_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/')
