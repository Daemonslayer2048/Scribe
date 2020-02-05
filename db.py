import sqlite3


def get_db_connection():
    database = "./Scribe.db"
    try:
        db_conn = sqlite3.connect(database)
        db_conn.row_factory = dict_factory
        db_conn.execute("PRAGMA foreign_keys = 1")
    except sqlite3.Error as e:
        print(e)
    return db_conn


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def run_query(query, values):
    con = get_db_connection()
    cur = con.cursor()
    try:
        cur.execute(query, values)
        con.commit()
        return cur.lastrowid, "No Error"
    except sqlite3.IntegrityError as e:
        con.close()
        return 406, e
    except sqlite3.OperationalError as e:
        con.close()
        return 409, e
    con.close()


def get_query(query, values):
    con = get_db_connection()
    cur = con.cursor()
    try:
        cur.execute(query, values)
        response = cur.fetchall()
        con.close()
        return response
    except Exception as e:
        return e
