import api
import flask
import os
import connexion
import re

app = connexion.App(__name__, specification_dir='./api')
app.add_api('swagger.yaml')

@app.route('/web')
def home():
    devices = api.devices.get()
    for device in devices:
        device.update({'model': api.models.get_devices_model(device['ip'])['model']})
    return flask.render_template("home.html", devices=devices)

@app.route('/web/config/<ip>')
def config(ip):
    config = api.devices.fetch(str(ip))
    config = config.split('\n')
    return flask.render_template("config.html", config=config)

if __name__ == '__main__':
    if not os.path.exists("./Scribe.db"):
        print("Building Database")
        db.build_db()
    app.run()
