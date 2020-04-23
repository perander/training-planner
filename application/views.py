from flask import render_template, request, redirect, url_for
from flask_login import current_user
from application import app, login_required
from application.tasks.models import Task


@app.route("/")
@login_required
def index():
    if current_user.admin:
        return redirect(url_for("tasks_index"))

    # new = Task.show_new_tasks(current_user)
    new = Task.query.all()
    inprogress = Task.show_tasksinprogress_by(current_user)
    return render_template("index.html",
                           new=new,
                           inprogress=inprogress)
