from datetime import datetime
from device_lib import *
from api import  *
import db

##############################################
# Definitions

def devices_to_collect():
    query = """
    Select
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
    Inner Join device_models on devices.model =  device_models.pk
    Where
	   enabled = 'True'
    ;"""
    values = []
    devices = db.get_query(query, values)
    return devices

def update_last_updated(device):
    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    query = """
    Update
        devices
    Set
        last_updated = ?
    Where
        pk = ?
    ;"""
    values = []
    values.append(timestamp)
    values.append(device['pk'])
    db.run_query(query, values)

def collect_device(device):
    if device['model'] == "Edge Switch":
        config = edgeswitch.get_config(device)
    elif device['model'] == "Edge Router":
        config = edgeos.get_config(device)
    else:
        print("Unknown device type")
    return config

##############################################
# Main
devices = devices_to_collect()
for device in devices:
    config = collect_device(device)
    with open("Configs/" + device['alias'], 'w') as file:
        file.write(config)
    update_last_updated(device)
