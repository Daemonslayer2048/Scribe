from flask import abort
import db
import os

def get():
    cur = db.get_db_connection().cursor()
    query = "SELECT ip, port, alias, model, enabled, last_updated FROM devices;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return

def delete(ip):
    #Remove device from DB
    query = """DELETE FROM devices WHERE ip = (?)"""
    db.run_query(query, (str(ip), ))
    print(str(ip))

def purge(ip):
    # Remove device from FS
    query = """
    SELECT
        alias
    FROM
        devices
    WHERE
        ip = (?)
    """
    alias = db.get_query(query, (ip, ))[0]['alias']
    if os.path.exists('./Configs/' + str(alias)):
        os.remove('./Configs/' + str(alias))
    #Remove device from DB
    query = """DELETE FROM devices WHERE alias = (?)"""
    db.run_query(query, (str(alias), ))

def add(node):
    required_list = ["ip", "alias", "model", "username", "password", "enabled"]
    missing_requireds = []
    # Ensure we get the values we are expecting and abort if values missing
    for required in required_list:
        if required not in node.keys():
            missing_requireds.append(required)
    if len(missing_requireds) > 0:
        abort(400, "You are missing the following required parameters: %s" % (str(missing_requireds)))
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

def fetch(ip):
    query = """
    SELECT
        alias
    FROM
        devices
    WHERE
        ip = (?)
    """
    alias = db.get_query(query, (ip, ))[0]['alias']
    try:
        config = open('./Configs/' + str(alias), "r").read()
    except FileNotFoundError as e:
        abort(406, "A config for this device does not exist yet!")
    return config

def disable(ip):
    query = """Update devices set enabled = False where ip = (?)"""
    db.run_query(query, (str(ip), ))
    print(str(ip))

def enable(ip):
    query = """Update devices set enabled = True where ip = (?)"""
    db.run_query(query, (str(ip), ))
    print(str(ip))
