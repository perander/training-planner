from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.tasks.models import Task
from application.tasks.forms import TaskForm


@app.route("/tasks", methods=["GET"])
def tasks_index():
    return render_template("tasks/list.html", tasks=Task.query.all())


@app.route("/*", methods=["POST"])
def tasks_search():
    param = request.form.get("query")

    found = Task.query.filter_by(name=param).all()

    if found is None or len(found) == 0:
        return render_template("notfound.html")

    return render_template("tasks/list.html", tasks=found)


# TODO: tiivistä allaolevat silleen 'if request.method = GET', sekä luodessa että päivittäessä

@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def tasks_create():
    if current_user.admin:
        if request.method == "GET":
            return render_template("tasks/new.html", form=TaskForm())

        form = TaskForm(request.form)

        if not form.validate():
            return render_template("tasks/new.html", form=form)

        t = Task(name=form.name.data,
                 description=form.description.data)

        db.session().add(t)
        db.session().commit()

    return redirect(url_for("tasks_index"))


@app.route("/update/<task_id>/", methods=["GET", "POST"])
@login_required
def tasks_update(task_id):
    if current_user.admin:
        if request.method == "GET":
            return render_template("tasks/updateform.html", task=Task.query.get(task_id))

        t = Task.query.get(task_id)
        t.name = request.form.get("newname")
        t.description = request.form.get("newdescription")

        db.session().commit()

    # lopulta jompi kumpi näistä:
    # return redirect(url_for("tasks_view"))
    # return render_template("tasks/taskinfo.html", task=Task.query.get(task_id))
    return redirect(url_for("tasks_index"))


@app.route("/delete/<task_id>", methods=["POST"])
@login_required
def tasks_delete(task_id):
    if current_user.admin:
        t = Task.query.get(task_id)

        db.session().delete(t)
        db.session().commit()

    return redirect(url_for("tasks_index"))


@app.route("/setdone/<task_id>/", methods=["POST"])
@login_required
def tasks_set_done(task_id):
    if current_user.admin:
        return redirect(url_for("tasks_index"))

    t = Task.query.get(task_id)
    t.done = True
    db.session().commit()  # actually updates the db

    return redirect(url_for("tasks_index"))
