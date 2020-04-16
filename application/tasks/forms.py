from flask_wtf import FlaskForm
from wtforms import StringField, validators
from application.forms import MultiCheckboxField
from application.category.models import Category
from application.tasks.models import Task


class TaskForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3)])
    description = StringField("Description")
    categories = MultiCheckboxField("Categories", choices=Category.query.all())
    subtasks = MultiCheckboxField("Subtasks", choices=Task.query.all())

    class Meta:
        csrf = False
