from flask import Blueprint
from ..models import Group
from .. import db

groups_bp = Blueprint('groups_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/web/groups')
