import db
from flask import abort

def get():
    models = get_models()
    cur = db.get_db_connection().cursor()
    query = "SELECT * FROM device_models;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return

def add(model):
    query = """INSERT INTO device_models (name) VALUES (?)"""
    db.run_query(query, (str(model), ))

def delete(model):
    query = """DELETE FROM device_models WHERE name = (?)"""
    response, e = db.run_query(query, (str(model), ))
    if response == 406:
        query = """SELECT COUNT(*) FROM device_models WHERE name = (?)"""
        response = db.get_query(query, (str(model), ))
        print(response)
        abort(406, "%s, there are %s device(s) using that model" % (str(e), str(response[0][0])))
    elif response == 409:
        abort(406, "%s" % (str(e)))

def get_devices_model(ip):
    cur = db.get_db_connection().cursor()
    query = """SELECT model FROM devices WHERE ip = (?)"""
    cur.execute(query, (ip, ))
    model_id = cur.fetchone()
    query = """SELECT model FROM device_models WHERE pk = (?)"""
    cur.execute(query, (model_id['model'], ))
    model = cur.fetchone()
    return model
