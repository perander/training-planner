from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.tasks.models import Task, tags
from application.tasks.forms import TaskForm

from application.auth.models import User
from application.category.models import Category


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


@app.route("/tasks/<task_id>/")
def tasks_view(task_id):
    categories = Category.query.join(tags).join(Task).filter(
        (tags.c.category_id == Category.id) & (tags.c.task_id == task_id)).all()

    # print("task tagged with: ", categories)

    return render_template("tasks/view.html", task=Task.query.get(task_id), categories=categories)


@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def tasks_create():
    if current_user.admin:
        if request.method == "GET":
            return render_template("tasks/new.html", form=TaskForm(), categories=Category.query.all())

        form = TaskForm(request.form)

        # TODO: multipleselectfield doesn't support form.validate, need custom validation
        # if not form.validate():
        #    return render_template("tasks/new.html", form=form)

        if form.is_submitted():
            t = Task(name=form.name.data,
                     description=form.description.data)

            for id in form.categories.data:
                c = Category.query.get(id)
                print("category: ", c.name)
                c.taskstagged.append(t)
                db.session.add(c)

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
        return redirect(url_for("tasks_index"))

    return render_template("tasks/view.html", task=Task.query.get(task_id))


@app.route("/deletetask/<task_id>", methods=["POST"])
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
    u = User.query.get(current_user.id)

    u.tasksdone.append(t)
    if t in u.tasksinprogress:
        u.tasksinprogress.remove(t)

    db.session().add(u)
    db.session().commit()  # actually updates the db

    return redirect(url_for("tasks_index"))


@app.route("/setinprogress/<task_id>/", methods=["POST"])
@login_required
def tasks_set_inprogress(task_id):
    if current_user.admin:
        return redirect(url_for("tasks_index"))

    t = Task.query.get(task_id)
    u = User.query.get(current_user.id)

    u.tasksinprogress.append(t)

    db.session().add(u)
    db.session().commit()  # actually updates the db

    return redirect(url_for("tasks_index"))
