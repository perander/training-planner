from flask_wtf import FlaskForm
from wtforms import StringField, validators


class TaskForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3)])
    description = StringField("Description")

    class Meta:
        csrf = False