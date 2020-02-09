from flask import abort
import db

def fetch(ip):
    query = """
    SELECT
	   devices.alias as alias,
	   repos.repo_name as repo
    FROM
	   devices
    INNER JOIN repos ON devices.repo = repos.repo_name
    WHERE
	   ip = (?)
    """
    device = db.get_query(query, (ip,))[0]
    file = "./Repositories/" + device["repo"] + "/" + device["alias"] + ".cfg"
    try:
        config = open(file, "r").read()
    except FileNotFoundError:
        abort(406, "A config for this device does not exist yet!")
    return config

def get():
    cur = db.get_db_connection().cursor()
    query = "SELECT ip, port, alias, model, enabled, last_updated FROM devices;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return
