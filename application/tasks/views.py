from application import app, db
from flask import redirect, render_template, request, url_for
from application.tasks.models import Task


@app.route("/tasks", methods=["GET"])
def tasks_index():
    return render_template("tasks/list.html", tasks=Task.query.all())


@app.route("/tasks/new/")
def tasks_form():
    return render_template("tasks/new.html")


@app.route("/tasks/<task_id>/", methods=["POST"])
def tasks_set_done(task_id):
    t = Task.query.get(task_id)
    t.done = True
    db.session().commit()  # actually updates the db

    return redirect(url_for("tasks_index"))


@app.route("/tasks/", methods=["POST"])
def tasks_create():
    t = Task(request.form.get("name"))

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("tasks_index"))


@app.route("/*", methods=["POST"])
def tasks_search():
    param = request.form.get("query")

    found = Task.query.filter_by(name=param).all()

    if found is None or len(found) == 0:
        return "Nothing found :("  # TODO: redirect to a not found page

    return render_template("tasks/list.html", tasks=found)


@app.route("/delete/<task_id>/", methods=["POST"])
def tasks_delete(task_id):
    t = Task.query.get(task_id)

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("tasks_index"))
