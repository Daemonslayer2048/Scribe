import sqlite3

users_table = """
CREATE TABLE users (
  'pk' INTEGER PRIMARY KEY,
  'username' TEXT NOT NULL UNIQUE,
  'group' INTEGER,
  CONSTRAINT fk_group
    FOREIGN KEY ('group')
    REFERENCES groups ('pk')
);
"""

groups_table = """
CREATE TABLE groups (
  'pk' INTEGER PRIMARY KEY,
  'groupname' TEXT NOT NULL UNIQUE
);
"""

device_models_table = """
CREATE TABLE device_models (
  'pk' INTEGER PRIMARY KEY,
  'manufacturer' TEXT NOT NULL,
  'model' TEXT NOT NULL,
  'OS' TEXT
);
"""

repos_table = """
CREATE TABLE repos (
	'pk' INTEGER PRIMARY KEY NOT NULL,
	'repo_name' TEXT NOT NULL
);
"""

remote_repos_table = """
CREATE TABLE remote_repos (
	'pk' INTEGER PRIMARY KEY NOT NULL,
	'name' TEXT NOT NULL,
	'URL' TEXT NOT NULL,
  	CONSTRAINT fk_name
  	  FOREIGN KEY ('name')
  	  REFERENCES repos ('name')
);
"""

proxies_tables = """
CREATE TABLE proxies (
	'pk' INTEGER PRIMARY KEY NOT NULL,
	'ip' TEXT NOT NULL,
  	'port' INT DEFAULT 22,
  	'username' TEXT NOT NULL,
    'password' TEXT NOT NULL
);
"""

devices_table = """
CREATE TABLE devices (
  'pk' INTEGER PRIMARY KEY,
  'ip' TEXT NOT NULL,
  'port' INT DEFAULT 22,
  'alias' TEXT,
  'model' TEXT NOT NULL,
  'user' TEXT,
  'username' TEXT NOT NULL,
  'password' TEXT NOT NULL,
  'enable' TEXT,
  'last_updated' TEXT NOT NULL DEFAULT "Never",
  'enabled' TEXT NOT NULL DEFAULT "True",
  'repo' TEXT NOT NULL DEFAULT 1,
  'proxy' INTEGER,
  CONSTRAINT fk_models
    FOREIGN KEY ('model')
    REFERENCES device_models ('pk'),
  CONSTRAINT fk_repo
  	FOREIGN KEY ('repo')
  	REFERENCES repos ('pk'),
  CONSTRAINT fk_proxy
    FOREIGN KEY ('proxy')
    REFERENCES proxies ('pk')
);"""


def build_db():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute(users_table)
    cur.execute(groups_table)
    cur.execute(device_models_table)
    cur.execute(repos_table)
    cur.execute(remote_repos_table)
    cur.execute(proxies_tables)
    cur.execute(devices_table)
    cur.execute("""INSERT INTO repos (repo_name) VALUES ('Default');""")
    con.commit()
    con.close()


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
        print(str(e))
        return 406, e
    except sqlite3.OperationalError as e:
        con.close()
        print(str(e))
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
