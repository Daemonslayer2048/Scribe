import os
from ruamel.yaml import YAML

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    config_file = str(basedir + "/config.yml")
    if os.path.isfile(config_file):
        with open(config_file, 'r') as file:
            yaml = YAML()
            config = yaml.load(file)
        # Get the SECRET_KEY
        SECRET_KEY = config['SECRET_KEY']
        # Get DB access
        SQLALCHEMY_DATABASE_URI = config['DATABASE_URI']
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        INSTALLED = True
    else:
        INSTALLED = False
