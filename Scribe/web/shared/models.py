from web import db
from web.models import *

def get_devices_model(alias):
    model = (db.session.query(Device, Device_model)
        .filter(Device.model == Device_model.id)
        .filter(Device.alias == str(alias))
        .first())
    return model
