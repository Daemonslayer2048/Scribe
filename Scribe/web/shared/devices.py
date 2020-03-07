from web import db
from web.models import *

def get_config(alias):
    repo = (db.session.query(Repo, Device)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.alias == alias)
        .first()).Repo.repo_name
    file = "./Repositories/" + repo + "/" + alias + ".cfg"
    try:
        config = open(file, "r").read()
    except FileNotFoundError:
        print("A config for this device does not exist yet!")
    return config
