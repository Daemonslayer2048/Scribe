from flask import abort
from Scribe import sqlite_db as db
import os


def get():
    cur = db.get_db_connection().cursor()
    query = """
    SELECT
        devices.pk As pk,
        devices.alias As alias,
        devices.ip As ip,
        devices.port As port,
        devices.enabled As enabled,
        devices.last_updated As last_updated,
        device_models.model As model,
        device_models.os As os,
        device_models.manufacturer As manufacturer,
        repos.repo_name as repo
    From
        devices
    Inner Join
        device_models on devices.model = device_models.pk,
        repos on devices.repo = repos.repo_name
    """
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return


def delete(alias):
    # Remove device from DB
    query = """DELETE FROM devices WHERE alias = (?)"""
    db.run_query(query, (str(alias),))
    print(str(alias))


def purge(alias):
    query = """
    SELECT
       devices.alias as alias,
       repos.repo_name as repo
    FROM
       devices
    INNER JOIN repos ON devices.repo = repos.repo_name
    WHERE
       alias = (?)
    """
    response = db.get_query(query, (alias,))[0]
    repo_dir = "./Repositories/" + response["repo"]
    config_file = repo_dir + "/" + response["alias"] + ".cfg"
    # Remove device from FS
    if os.path.exists(config_file):
        os.remove(config_file)
    # Remove device from DB
    query = """DELETE FROM devices WHERE alias = (?)"""
    db.run_query(query, (str(alias),))


def add(node):
    required_list = ["ip", "alias", "model", "username", "password", "enabled"]
    missing_requireds = []
    # Ensure we get the values we are expecting and abort if values missing
    for required in required_list:
        if required not in node.keys():
            missing_requireds.append(required)
    if len(missing_requireds) > 0:
        abort(
            400,
            "You are missing the following required parameters: %s"
            % (str(missing_requireds)),
        )
    values = []
    values.append(node["ip"])
    if "port" not in node.keys():
        values.append("22")
    else:
        values.append(node["port"])
    values.append(node["alias"])
    values.append(node["model"])
    values.append(node["username"])
    values.append(node["password"])
    if "enable" not in node.keys():
        values.append(None,)
    else:
        values.append(node["enable"])
    if "enabled" not in node.keys():
        values.append(True)
    else:
        values.append(node["enabled"])
    query = """INSERT INTO devices (ip, port, alias, model, username, password, enable, enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    response, e = db.run_query(query, values)
    if response == 406:
        if "UNIQUE constraint failed" in str(e):
            print(e)
            abort(406, "A device by this name already exists")
        elif "FOREIGN KEY constraint failed" in str(e):
            print(e)
            abort(406, "Does this client exist in db already?")


def get_config(alias):
    query = """
    SELECT
        repos.repo_name as repo
    FROM
        devices
    INNER JOIN repos ON devices.repo = repos.repo_name
    WHERE
        alias = (?)
    """
    repo = db.get_query(query, (str(alias),))[0]["repo"]
    file = "./Repositories/" + repo + "/" + alias + ".cfg"
    try:
        config = open(file, "r").read()
    except FileNotFoundError:
        abort(406, "A config for this device does not exist yet!")
    return config


def disable(alias):
    query = """Update devices set enabled = False where alias = (?)"""
    db.run_query(query, (str(alias),))


def enable(alias):
    query = """Update devices set enabled = True where alias = (?)"""
    db.run_query(query, (str(alias),))
