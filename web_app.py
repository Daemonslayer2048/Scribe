from api import *
import flask
import api
import connexion

app = connexion.App(__name__, specification_dir='./')
app.add_api('swagger.yaml')

@app.route('/hello')
def hello_web():
    return "Hello!"

@app.route('/')
def home():
    devices = api.devices.get()
    for device in devices:
        device.update({'model': models.get_devices_model(device['ip'])['model']})
    return flask.render_template("home.html", devices=devices)

if __name__ == '__main__':
    app.run()
