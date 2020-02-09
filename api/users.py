import db

def get_users():
    cur = db.get_db_connection().cursor()
    query = "SELECT * FROM users;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return


def get():
    users = get_users()
    return [users][0]


def add(user):
    query = """INSERT INTO users (username) VALUES (?)"""
    db.run_query(query, (str(user),))


def delete(user):
    query = """DELETE FROM users WHERE username = (?)"""
    db.run_query(query, (str(user),))
