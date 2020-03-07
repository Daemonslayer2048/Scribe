from Scribe.web import db
from Scribe.web.models import *

def get_device_repo(alias):
    repo = (db.session.query(Device, Repo)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.alias == str(alias))
        .first())
    return repo
