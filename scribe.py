from datetime import datetime
from dulwich import porcelain
from device_lib import *
from api import *
import os
import db

##############################################
# Definitions
def devices_to_collect():
    query = """SELECT
        devices.pk As pk,
        devices.ip As ip,
        devices.port As port,
        devices.alias As alias,
        devices.username As username,
        devices.password As password,
        devices.enable As enable,
        device_models.model As model,
        devices.enabled As enabled
    From
        devices
    Inner Join
        device_models on devices.model =  device_models.pk
    Where
        enabled = 1;"""
    values = []
    devices = db.get_query(query, values)
    return devices


def update_last_updated(device, timestamp):
    query = """UPDATE
        devices
    SET
        last_updated = (?)
    WHERE
        pk = (?);"""
    values = []
    values.append(timestamp)
    values.append(device["pk"])
    db.run_query(query, values)


def collect_device(device):
    if device["model"] == "Edge Switch":
        config = edgeswitch.get_config(device)
    elif device["model"] == "Edge Router":
        config = edgeos.get_config(device)
    else:
        print("Unknown device type")
    return config

##############################################
# Main
devices = devices_to_collect()
for device in devices:
    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    config = collect_device(device)
    alias = str(device["alias"]).replace(" ", "_")
    repo_dir = "./Repositories/" + alias
    config_file = repo_dir + "/" + alias + ".cfg"
    if not os.path.isdir(repo_dir):
        repo = porcelain.init(repo_dir)
    else:
        repo = porcelain.open_repo(repo_dir)
    with open(config_file, "w") as file:
        file.write(config)
    porcelain.add(repo, config_file)
    porcelain.commit(repo, b"A sample commit")
    update_last_updated(device, timestamp)
