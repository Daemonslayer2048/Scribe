from Scribe import db

def get_repos():
    cur = db.get_db_connection().cursor()
    query = "SELECT * FROM repos;"
    cur.execute(query)
    db_return = cur.fetchall()
    return db_return


def get():
    repos = get_repos()
    return [repos][0]


def add(repo_name):
    query = """INSERT INTO repos (repo_name) VALUES (?)"""
    db.run_query(query, (str(repo_name["repo_name"]), ))


def delete(repo_name):
    query = """DELETE FROM repos WHERE repo_name = (?)"""
    db.run_query(query, (str(repo_name),))

def get_device_repo(alias):
    cur = db.get_db_connection().cursor()
    query = """
    SELECT
        repos.repo_name as repo
    FROM
        devices
    INNER JOIN repos ON devices.repo = repos.repo_name
    WHERE
        alias = (?)
    """
    cur.execute(query, (str(alias),))
    response = cur.fetchone()
    return response

def get_repo_devices(repo_name):
    query = """
    SELECT
        devices.alias as alias,
        devices.ip as ip,
        device_models.model as model
    FROM
        devices
    INNER JOIN
        repos ON devices.repo = repos.repo_name,
        device_models ON devices.model = device_models.pk
    WHERE
        repos.repo_name = (?)
    """
    response = db.get_query(query, (str(repo_name), ))
    return response
