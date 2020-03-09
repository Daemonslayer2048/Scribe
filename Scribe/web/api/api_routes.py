from flask_login import current_user, login_user, logout_user, login_required
from flask_restx import Resource, Api, fields
from dataclasses import dataclass
from flask import Blueprint
from flask import jsonify
import flask
import os
from . import db
from . import Device, Repo, Device_model, User

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, version='1.0', title='Scribe API',
    description='An API for interfacing with Scribe',
)
###################################################
#                     Devices                     #
###################################################
devices_ns = api.namespace('devices', description='Device Operations')
add_device = api.parser()
add_device.add_argument(
    "ip", type=str, required=True, help="Device Ip Address", location="form"
)
add_device.add_argument(
    "port", type=int, required=False, default=22, help="Device ssh port, defaults to 22 if not provided.", location="form"
)
add_device.add_argument(
    "alias", type=str, required=True, help="A uniquie device alias", location="form"
)
add_device.add_argument(
    "model", type=int, required=True, help="The ID of the model to be used, you will need to check a different endpoint to get all model IDs.", location="form"
)
add_device.add_argument(
    "username", type=str, required=True, help="SSH Username", location="form"
)
add_device.add_argument(
    "password", type=str, required=True, help="SSH Password", location="form"
)
add_device.add_argument(
    "enable", type=str, required=False, help="Devices enable password, if it exists", location="form"
)
add_device.add_argument(
    "enabled", type=str, required=True, help="Enable device config collection, must be a True or False.", location="form"
)
add_device.add_argument(
    "repo", type=str, required=False, default="Default", help="Defaults to repo Default, if not provided", location="form"
)
@devices_ns.route("")
class Devices(Resource):
    @devices_ns.doc(parser=add_device, description="Add a device")
    def post(Resource):
        args = add_device.parse_args()
        #Args check
        if args.enabled.lower() == "true":
            enabled = True
        elif args.enabled.lower() == "false":
            enabled = False
        else:
            return str("Invalid enabled parameter, recieved: %s" % (args.enabled)), 400
        try:
            device = Device(
                ip=args.ip,
                port=args.port,
                alias=args.alias,
                model=args.model,
                user=args.username,
                password=args.password,
                enable=args.enable,
                enabled=enabled,
                repo=args.repo
            )
            db.session.add(device)
            db.session.commit()
            return "Adding device succeeded"
        except Exception as e:
            print(e)
            return "Adding device failed"
    @devices_ns.doc(description="Get all devices")
    def get(Resource):
        devices = []
        response = (db.session.query(Device, Repo, Device_model)
            .filter(Device.repo == Repo.repo_name)
            .filter(Device.model == Device_model.id)
            .all())
        for row in response:
            device = {}
            device['ip'] = row.Device.ip
            device['port'] = row.Device.port
            device['alias'] = row.Device.alias
            device['last_updated'] = row.Device.last_updated
            device['enabled'] = row.Device.enabled
            device['manufacturer'] = row.Device_model.manufacturer
            device['model'] = row.Device_model.model
            device['repo'] = row.Repo.repo_name
            devices.append(device)
        return jsonify(devices)

@devices_ns.route("/<string:alias>")
@devices_ns.doc(description="Remove a device")
class Device_removal(Resource):
    def delete(Resource, alias):
        try:
            Device.query.filter(Device.alias == alias).delete()
            db.session.commit()
        except Exception as e:
            print(e)
        return "Operation Complete"

@devices_ns.route("/purge/<string:alias>")
@devices_ns.doc(description="Purge a device and its config from Scribe")
class Device_removal(Resource):
    def delete(Resource, alias):
        response = db.session.query(Device, Repo).filter(Device.repo == Repo.repo_name).first()
        repo_dir = "./Repositories/" + response.Repo.repo_name
        config_file = repo_dir + "/" + alias + ".cfg"
        try:
            Device.query.filter(Device.alias == alias).delete()
            db.session.commit()
        except Exception as e:
            print(e)
        if os.path.exists(config_file):
            os.remove(config_file)
            return "Operation Complete"
        else:
            return "Config file did not exist, device removed from database."

@devices_ns.route("/enable/<string:alias>")
@devices_ns.doc(description="Enable a device for config collection")
class Device_enable(Resource):
    def put(Resource, alias):
        query = db.session.query(Device).filter(Device.alias == alias).update({'enabled': True})
        db.session.commit()
        return str("Device %s enabled" % (alias))


@devices_ns.route("/disable/<string:alias>")
@devices_ns.doc(description="Disable a device for config collection")
class Device_disable(Resource):
    def put(Resource, alias):
        query = db.session.query(Device).filter(Device.alias == alias).update({'enabled': False})
        db.session.commit()
        return str("Device %s disabled" % (alias))

@devices_ns.route("/config/<string:alias>")
@devices_ns.doc(description="Get a devices most recent config")
class Device_config(Resource):
    def get(Resource, alias):
        response = db.session.query(Device, Repo).filter(Device.repo == Repo.repo_name).first()
        repo_dir = "./Repositories/" + response.Repo.repo_name
        config_file = repo_dir + "/" + alias + ".cfg"
        try:
            config = open(config_file, "r").read()
            return config
        except FileNotFoundError:
            return "A config for this device does not exist yet!"

@devices_ns.route("/config/<string:alias>/<string:hash>")
@devices_ns.doc(description="Get a devices most recent config")
class Device_config(Resource):
    def get(Resource, alias):
        response = db.session.query(Device, Repo).filter(Device.repo == Repo.repo_name).first()
        repo_dir = "./Repositories/" + response.Repo.repo_name
        config_file = repo_dir + "/" + alias + ".cfg"
        try:
            config = open(config_file, "r").read()
            return config
        except FileNotFoundError:
            return "A config for this device does not exist yet!"


###################################################
#               Oxidized Compatible               #
###################################################

###################################################
#                     Users                       #
###################################################

###################################################
#                     Groups                       #
###################################################

###################################################
#                     Models                      #
###################################################

###################################################
#                      Repos                      #
###################################################

###################################################
#                      Users                      #
###################################################
users_ns = api.namespace('users', description='User Operations')
@users_ns.route("")
class Users(Resource):
    def get(Resource):
        users = []
        response = User.query.all()
        for row in response:
            user = {}
            user['username'] = row.username
            user['email'] = row.email
            user['group'] = row.group
            users.append(user)
        return jsonify(users)

###################################################
#                       Web                       #
###################################################

###################################################
#                      Hello                      #
###################################################
hello_ns = api.namespace('', description='Hello World Operations')

@hello_ns.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return "Hello"
