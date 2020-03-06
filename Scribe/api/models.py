from Scribe import db
from flask import abort


def get():
    cur = db.get_db_connection().cursor()
    query = "SELECT * FROM device_models;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return


def add(model):
    values = []
    values.append(model["OS"])
    values.append(model["manufacturer"])
    values.append(model["model"])
    query = """INSERT INTO device_models (OS, manufacturer, model) VALUES (?, ?, ?)"""
    db.run_query(query, values)


def delete(pk):
    query = """DELETE FROM device_models WHERE pk = (?)"""
    response, e = db.run_query(query, (str(pk),))
    if response == 406:
        query = """SELECT COUNT(*) FROM device_models WHERE pk = (?)"""
        response = db.get_query(query, (str(pk),))
        print(response)
        abort(
            406,
            "%s, there are %s device(s) using that model"
            % (str(e), str(response[0]["COUNT(*)"])),
        )
    elif response == 409:
        abort(406, "%s" % (str(e)))


def get_devices_model(alias):
    cur = db.get_db_connection().cursor()
    query = """
        SELECT device_models.manufacturer as "manufacturer", device_models.model as "model", device_models.OS as "OS" FROM devices INNER JOIN device_models ON devices.model = device_models.pk WHERE devices.alias = (?) """
    cur.execute(query, (str(alias),))
    response = cur.fetchone()
    return response
