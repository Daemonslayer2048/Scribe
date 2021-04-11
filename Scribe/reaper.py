#! python3
from datetime import datetime
from web import db
from web.models import Device, Device_model, Repo
from web.shared import git
from device_lib import *
import argparse

##############################################
# Definitions


def reap_device_config(device):
    if device.Device_model.os == "EdgeSwitch":
        config = edgeswitch.get_config(device)
    elif device.Device_model.os == "EdgeOS":
        config = edgeos.get_config(device)
    elif device.Device_model.os == "JunOS":
        config = junos.get_config(device)
    else:
        print("Unknown device type")
    return config


def log_config_collection(alias, timestamp):
    db.session.query(Device).filter(Device.alias == alias).update(
        {"last_updated": timestamp}
    )
    db.session.commit()


##########################################################################
#  ArgumentParser
parser = argparse.ArgumentParser(
    prog="PROG",
    description="""""",
    epilog="""""",
)
parser.add_argument(
    "-d",
    "--device",
    help="",
)
args = parser.parse_args()

##############################################
# Main
if args.device:
    device = (
        db.session.query(Device, Repo, Device_model)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.model == Device_model.id)
        .filter(Device.alias == args.device)
        .first()
    )
    repo_dir = "./Repositories/" + device.Repo.repo_name
    config_file = repo_dir + "/" + device.Device.alias + ".cfg"
    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    config = reap_device_config(device)
    repo = git.get_repo(repo_dir)
    with open(config_file, "w") as file:
        file.write(config)
    git.add(repo, device.Device.alias)
    git.commit_to_repo(repo)
    log_config_collection(device.Device.alias, timestamp)
else:
    devices = (
        db.session.query(Device, Repo, Device_model)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.model == Device_model.id)
        .filter(Device.enabled == True)
        .all()
    )
    for device in devices:
        repo_dir = "./Repositories/" + device.Repo.repo_name
        config_file = repo_dir + "/" + device.Device.alias + ".cfg"
        timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        config = reap_device_config(device)
        repo = git.get_repo(repo_dir)
        with open(config_file, "w") as file:
            file.write(config)
        git.add(repo, device.Device.alias)
        git.commit_to_repo(repo)
        log_config_collection(device.Device.alias, timestamp)
