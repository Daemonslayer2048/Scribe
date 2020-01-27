import db

def get_clients():
    cur = db.get_db_connection().cursor()
    query = "SELECT * FROM clients;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return

def get():
    clients = get_clients()
    return [clients]

def add(client):
    query = """INSERT INTO clients (name) VALUES (?)"""
    db.run_query(query, (str(client), ))

def delete(client):
    query = """DELETE FROM clients WHERE name = (?)"""
    db.run_query(query, (str(client), ))
