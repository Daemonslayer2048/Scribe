from flask_restx import Resource, Api
from flask import Blueprint
from flask import jsonify
from flask import make_response
import os
from . import db
from . import Device, Repo, Device_model, User, Group
from ..shared import git

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(
    api_bp,
    version="1.0",
    title="Scribe API",
    description="An API for interfacing with Scribe",
    default_mediatype="application/json",
)
###################################################
#                     Devices                     #
###################################################
devices_ns = api.namespace("devices", description="Device Operations")
add_device = api.parser()
add_device.add_argument(
    "ip", type=str, required=True, help="Device Ip Address", location="form"
)
add_device.add_argument(
    "port",
    type=int,
    required=False,
    default=22,
    help="Device ssh port, defaults to 22 if not provided.",
    location="form",
)
add_device.add_argument(
    "alias", type=str, required=True, help="A uniquie device alias", location="form"
)
add_device.add_argument(
    "model",
    type=int,
    required=True,
    help="The ID of the model to be used, you will need to check a different endpoint to get all model IDs.",
    location="form",
)
add_device.add_argument(
    "username", type=str, required=True, help="SSH Username", location="form"
)
add_device.add_argument(
    "password", type=str, required=True, help="SSH Password", location="form"
)
add_device.add_argument(
    "enable",
    type=str,
    required=False,
    help="Devices enable password, if it exists",
    location="form",
)
add_device.add_argument(
    "enabled",
    type=str,
    required=True,
    help="Enable device config collection, must be a True or False.",
    location="form",
)
add_device.add_argument(
    "repo",
    type=str,
    required=False,
    default="Default",
    help="Defaults to repo Default, if not provided",
    location="form",
)


@devices_ns.route("")
class Devices(Resource):
    @devices_ns.doc(parser=add_device, description="Add a device")
    def post(Resource):
        args = add_device.parse_args()
        # Args check
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
                repo=args.repo,
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
        response = (
            db.session.query(Device, Repo, Device_model)
            .filter(Device.repo == Repo.repo_name)
            .filter(Device.model == Device_model.id)
            .all()
        )
        for row in response:
            device = {}
            device["ip"] = row.Device.ip
            device["port"] = row.Device.port
            device["alias"] = row.Device.alias
            device["last_updated"] = row.Device.last_updated
            device["enabled"] = row.Device.enabled
            device["manufacturer"] = row.Device_model.manufacturer
            device["model"] = row.Device_model.model
            device["repo"] = row.Repo.repo_name
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
        response = (
            db.session.query(Device, Repo).filter(Device.repo == Repo.repo_name).first()
        )
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
        query = (
            db.session.query(Device)
            .filter(Device.alias == alias)
            .update({"enabled": True})
        )
        db.session.commit()
        return str("Device %s enabled" % (alias))


@devices_ns.route("/disable/<string:alias>")
@devices_ns.doc(description="Disable a device for config collection")
class Device_disable(Resource):
    def put(Resource, alias):
        query = (
            db.session.query(Device)
            .filter(Device.alias == alias)
            .update({"enabled": False})
        )
        db.session.commit()
        return str("Device %s disabled" % (alias))


@devices_ns.route("/config/<string:alias>")
@devices_ns.doc(description="Get a devices most recent config")
class Device_config(Resource):
    def get(Resource, alias):
        response = (
            db.session.query(Device, Repo).filter(Device.repo == Repo.repo_name).first()
        )
        repo_dir = "./Repositories/" + response.Repo.repo_name
        config_file = repo_dir + "/" + alias + ".cfg"
        try:
            # JSON can not be retuned here for obviouse reasons
            # Instead flask esponse is used to create the correct response and response type
            # Swagger will claim response type is application/json, unknown how to change this
            config = open(config_file, "r").read()
            response = make_response(config)
            response.headers['content-type'] = 'text/plain'
            return response
        except FileNotFoundError:
            return "A config for this device does not exist yet!"


@devices_ns.route("/config/<string:alias>/<string:hash>")
@devices_ns.doc(description="Get a devices most recent config (NOT DONE YET)")
class Device_config_at_hash(Resource):
    def get(Resource, alias, hash):
        config = git.get_config_at_hash(alias, hash)
        response = make_response(config)
        response.headers['content-type'] = 'text/plain'
        return response

@devices_ns.route("/config/<string:alias>/get_git_log")
@devices_ns.doc(description="Get a devices git log")
class Device_config_git_logs(Resource):
    def get(Resource, alias):
        response = (
            db.session.query(Device, Repo).filter(Device.repo == Repo.repo_name).first()
        )
        repo_dir = "./Repositories/" + response.Repo.repo_name
        config_file = repo_dir + "/" + response.Device.alias + ".cfg"
        commits = git.get_device_git_log(response.Device.alias)
        return commits

@devices_ns.route("/<string:alias>")
class Device_single(Resource):
    @devices_ns.doc(description="Get a device")
    def get(Resource, alias):
        response = (
            db.session.query(Device, Repo, Device_model)
            .filter(Device.repo == Repo.repo_name)
            .filter(Device.model == Device_model.id)
            .filter(Device.alias == alias)
            .first()
        )
        device = {}
        device["ip"] = response.Device.ip
        device["port"] = response.Device.port
        device["alias"] = response.Device.alias
        device["last_updated"] = response.Device.last_updated
        device["enabled"] = response.Device.enabled
        device["manufacturer"] = response.Device_model.manufacturer
        device["model"] = response.Device_model.model
        device["repo"] = response.Repo.repo_name
        return jsonify(device)


###################################################
#               Oxidized Compatible               #
###################################################
oxidized_ns = api.namespace("oxidized", description="Oxidized Compatible API endpoints")


@oxidized_ns.route("/nodes")
class Oxidized_Nodes(Resource):
    def get(Resource):
        devices = []
        response = (
            db.session.query(Device, Repo, Device_model)
            .filter(Device.repo == Repo.repo_name)
            .filter(Device.model == Device_model.id)
            .all()
        )
        for row in response:
            device = {}
            device["ip"] = row.Device.ip
            device["port"] = row.Device.port
            device["alias"] = row.Device.alias
            device["last_updated"] = row.Device.last_updated
            device["enabled"] = row.Device.enabled
            device["manufacturer"] = row.Device_model.manufacturer
            device["model"] = row.Device_model.model
            device["repo"] = row.Repo.repo_name
            devices.append(device)
        return jsonify(devices)


@oxidized_ns.route("/node/fetch/<string:ip>")
class Oxidized_config(Resource):
    def get(Resource, ip):
        response = (
            db.session.query(Device, Repo, Device_model)
            .filter(Device.repo == Repo.repo_name)
            .filter(Device.model == Device_model.id)
            .filter(Device.ip == ip)
            .first()
        )
        file = "./Repositories/" + response.Repo.repo_name + "/" + response.Device.alias + ".cfg"
        try:
            config = open(file, "r").read()
            return config
        except FileNotFoundError:
            return "Config not found", 500


###################################################
#                     Groups                       #
###################################################
groups_ns = api.namespace("groups", description="User Operations")


@groups_ns.route("")
class Groups(Resource):
    def get(Resource):
        groups = []
        response = Group.query.all()
        for row in response:
            group = {}
            group["groupname"] = row.groupname
            groups.append(group)
        return jsonify(groups)


@groups_ns.route("<string:group_name>")
class Groups_ops(Resource):
    def put(Resource, group_name):
        group = Group(groupname=group_name)
        db.session.add(group)
        db.session.commit()
        return str("Group %s added" % (group_name))

    def delete(Resource, group_name):
        Group.query.filter(Group.groupname == group_name).delete()
        db.session.commit()
        return str("Group %s removed" % (group_name))


###################################################
#                     Models                      #
###################################################
models_ns = api.namespace("models", description="User Operations")
add_model = api.parser()
add_model.add_argument(
    "manufacturer",
    type=str,
    required=True,
    help="Manufacturer of the device.......duh",
    location="form",
)
add_model.add_argument(
    "model", type=str, required=True, help="Model of the device", location="form"
)
add_model.add_argument(
    "os",
    type=str,
    required=True,
    help="Operating System of the device",
    location="form",
)


@models_ns.route("")
class Device_models(Resource):
    def get(Resource):
        models = []
        response = Device_model.query.all()
        for row in response:
            model = {}
            model["id"] = row.id
            model["manufacturer"] = row.manufacturer
            model["model"] = row.model
            model["os"] = row.os
            models.append(model)
        return jsonify(models)

    @models_ns.doc(parser=add_model, description="Add a device model")
    def post(Resource):
        args = add_model.parse_args()
        model = Device_model(
            manufacturer=args.manufacturer, model=args.model, os=args.os
        )
        db.session.add(model)
        db.session.commit()
        return "Adding device model succeeded"


@models_ns.route("<string:model_id>")
class Models_ops(Resource):
    def delete(Resource, model_id):
        Device_model.query.filter(Device_model.id == model_id).delete()
        db.session.commit()
        return str("Model %s removed" % (model_id))


###################################################
#                      Repos                      #
###################################################
repos_ns = api.namespace("repos", description="User Operations")


@repos_ns.route("")
class Repos(Resource):
    def get(Resource):
        repos = []
        response = Repo.query.all()
        for row in response:
            repo = {}
            repo["id"] = row.id
            repo["repo_name"] = row.repo_name
            repos.append(repo)
        return jsonify(repos)


@repos_ns.route("<string:repo_name>")
class Repo_Ops(Resource):
    def put(Resource, repo_name):
        repo = Repo(repo_name=repo_name)
        db.session.add(repo)
        db.session.commit()
        return str("Repo %s added" % (repo_name))

    def delete(Resource, repo_name):
        Repo.query.filter(Repo.repo_name == repo_name).delete()
        db.session.commit()
        return str("Repo %s removed" % (repo_name))

###################################################
#                      Users                      #
###################################################
users_ns = api.namespace("users", description="User Operations")
add_user = api.parser()
add_user.add_argument(
    "username",
    type=str,
    required=True,
    help="Users username.......duh",
    location="form",
)
add_user.add_argument(
    "email", type=str, required=True, help="Users full email", location="form"
)
add_user.add_argument(
    "group", type=str, required=False, help="Group to add user to", location="form"
)
add_user.add_argument(
    "password", type=str, required=True, help="Users password", location="form"
)


@users_ns.route("")
class Users(Resource):
    def get(Resource):
        users = []
        response = User.query.all()
        for row in response:
            user = {}
            user["username"] = row.username
            user["email"] = row.email
            user["group"] = row.group
            users.append(user)
        return jsonify(users)

    @users_ns.doc(parser=add_user, description="Add a user")
    def post(Resource):
        args = add_user.parse_args()
        user = User(username=args.username, email=args.email, group=args.group)
        user.set_password(str(args.password))
        db.session.add(user)
        db.session.commit()
        return "Adding user succeeded"


@users_ns.route("<string:user_name>")
class Users_ops(Resource):
    def delete(Resource, user_name):
        User.query.filter(User.username == user_name).delete()
        db.session.commit()
        return str("User %s removed" % (user_name))


###################################################
#                       Web                       #
###################################################
api_web_ns = api.namespace("web_api", description="Endpoints for web")

@api_web_ns.route("/config/<string:alias>/<string:hash>")
class web_api(Resource):
    def get(Resource, alias, hash):
        config = git.get_config_at_hash(alias, hash)
        html = """"""
        html += "<tbody>" + "\n"
        for line in config.splitlines():
            config_line = "<tr> <td> " + str(line).rstrip() + " </td> </tr>" + "\n"
            html += config_line
        html += "</tbody>"
        response = make_response(str(html))
        response.headers['content-type'] = 'text/html'
        return response
###################################################
#                      Hello                      #
###################################################
hello_ns = api.namespace("", description="Hello World Operations")


@hello_ns.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return "Hello"
