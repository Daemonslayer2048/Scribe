from flask import Blueprint
from ..models import Repo, Device, Device_Model
from .. import db

repo_bp = Blueprint(
    "repo_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/web/repos",
)
