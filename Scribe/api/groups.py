from Scribe import db
from flask import abort

def get_groups():
    cur = db.get_db_connection().cursor()
    query = "SELECT * FROM groups;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return


def get():
    groups = get_groups()
    return [groups][0]


def add(group):
    query = """INSERT INTO groups (groupname) VALUES (?)"""
    db.run_query(query, (str(group),))


def delete(group):
    query = """DELETE FROM groups WHERE groupname = (?)"""
    db.run_query(query, (str(group),))
