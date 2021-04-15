from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class NewDeviceForm(FlaskForm):
    ip = StringField("IP", validators=[DataRequired()])
    port = StringField("Port", validators=[DataRequired()])
    alias = StringField("Alias", validators=[DataRequired()])
    enabled = BooleanField("Enabled", validators=[DataRequired()])
    manufacturer = StringField("Manufacturer", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])
    repo = StringField("Repository", validators=[DataRequired()])
    submit = SubmitField("Add Device")
