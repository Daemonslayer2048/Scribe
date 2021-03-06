from . import db
from .models import *
from . import repos
import os
from sh import git


def get_repo(repo_dir):
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
    repo = git.bake(_cwd=repo_dir)
    repo.init()
    return repo


def get_git_log(repo, config_file):
    log = repo.log(
        "--pretty=format:%h:%an:%ai:%s", "--follow", config_file, _tty_out=False
    )
    commits = []
    for line in log:
        commit = {}
        commit["Hash"] = line.split(":")[0]
        commit["Author"] = line.split(":")[1]
        commit["Date"] = (
            line.split(":")[2] + ":" + line.split(":")[3] + ":" + line.split(":")[4]
        )
        commit["Message"] = line.rstrip().split(":")[5]
        commits.append(commit)
    return commits


def commit_to_repo(repo, message="No message"):
    try:
        repo.commit(m=message)
    except Exception as e:
        if "nothing to commit, working tree clean" in str(e):
            print("No change to repository!")


def add(repo, config):
    repo.add(config + ".cfg")


def get_device_git_log(alias):
    repo_name = (
        db.session.query(Repo, Device)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.alias == alias)
        .first()
    ).Repo.repo_name
    repo = get_repo(str("./Repositories/" + repo_name))
    log = get_git_log(repo, alias + ".cfg")
    return log


def get_config_at_hash(alias, hash):
    repo_name = repos.get_device_repo(alias).Repo.repo_name
    repo = get_repo(str("./Repositories/" + repo_name))
    show = hash + ":" + alias + ".cfg"
    config = repo.show(show, _tty_out=False)
    return str(config)
