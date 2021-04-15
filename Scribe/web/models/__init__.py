from ..forms import LoginForm, SignupForm
from .. import db
from .. import login
from .device_associations import Device_Associations
from .device_model import Device_Model
from .device import Device
from .group_associations import Group_Associations
from .group import Group
from .proxy import Proxy
from .repo import Repo
from .user import User


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
