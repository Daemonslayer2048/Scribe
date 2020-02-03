import db
from flask import abort

def get():
    cur = db.get_db_connection().cursor()
    query = "SELECT * FROM devices;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return

def delete(ip):
    query = """DELETE FROM devices WHERE name = (?)"""
    db.run_query(query, (str(ip), ))

def add(ip, device):
    required_list = ["client", "model", "password", "username"]
    missing_requireds = []
    # Ensure we get the values we are expecting and abort if values missing
    for required in required_list:
        if required not in device.keys():
            missing_requireds.append(required)
    if len(missing_requireds) > 0:
        abort(400, "You are missing the following required parameters: %s" % (str(missing_requireds)))
    values = []
    values.append(ip)
    values.append(device["client"])
    values.append(device["model"])
    values.append(device["password"])
    values.append(device["username"])
    if "alias" in device.keys():
        values.append(device["alias"])
    else:
        values.append("")
    if "enable" in device.keys():
        values.append(device["enable"])
    else:
        values.append("")
    query = """INSERT INTO devices (name, client, model, password, username, alias, enable) VALUES (?, ?, ?, ?, ?, ?, ?)"""
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
    config = open('./Configs/' + str(alias), "r").read()
    return config
