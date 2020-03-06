#! python3
from datetime import datetime
from device_lib import *
from api import *
import argparse
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
        device_models.OS As OS,
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


def get_device_info(device):
    query = """SELECT
        devices.pk As pk,
        devices.ip As ip,
        devices.port As port,
        devices.alias As alias,
        devices.username As username,
        devices.password As password,
        devices.enable As enable,
        device_models.OS As OS,
        devices.enabled As enabled
    From
        devices
    Inner Join
        device_models on devices.model =  device_models.pk
    Where
        enabled = 1 and devices.alias = (?)"""
    values = [device]
    device_info = db.get_query(query, values)
    return device_info


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
    if device["OS"] == "EdgeSwitch":
        config = edgeswitch.get_config(device)
    elif device["OS"] == "EdgeOS":
        config = edgeos.get_config(device)
    elif device["OS"] == "JunOS":
        config = junos.get_config(device)
    else:
        print("Unknown device type")
    return config


##########################################################################
#  ArgumentParser
parser = argparse.ArgumentParser(prog="PROG", description="""""", epilog="""""",)
parser.add_argument(
    "-d", "--device", help="",
)
args = parser.parse_args()

##############################################
# Main
if args.device:
    device = args.device
    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    device_info = get_device_info(device)[0]
    repo = str(repos.get_device_repo(device)["repo"])
    repo_dir = "./Repositories/" + repo
    config_file = repo_dir + "/" + device + ".cfg"
    config = collect_device(device_info)
    repo = git.get_repo(repo_dir)
    with open(config_file, "w") as file:
        file.write(config)
    git.add(repo, device)
    git.commit_to_repo(repo)
    update_last_updated(device_info, timestamp)
else:
    devices = devices_to_collect()
    for device in devices:
        timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        config = collect_device(device)
        query = """
        SELECT
            repos.repo_name as repo
        FROM
            devices
        INNER JOIN repos ON devices.repo = repos.repo_name
        WHERE
            alias = (?)
        """
        repo = db.get_query(query, (device["alias"],))[0]["repo"]
        repo_dir = "./Repositories/" + repo
        config_file = repo_dir + "/" + device["alias"] + ".cfg"
        repo = git.get_repo(repo_dir)
        with open(config_file, "w") as file:
            file.write(config)
        git.add(repo, device["alias"])
        git.commit_to_repo(repo)
        update_last_updated(device, timestamp)
