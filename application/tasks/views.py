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

    return render_template("tasks/view.html", task=Task.query.get(task_id), categories=categories)


@app.route("/tasks/new", methods=["GET", "POST"])
@login_required
def tasks_create():
    if current_user.admin:
        if request.method == "GET":
            return render_template("tasks/new.html",
                                   form=TaskForm(),
                                   categories=Category.query.all(),
                                   tasks=Task.query.all())

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

            print("subtasks ", form.subtasks.data)

            for id in form.subtasks.data:
                s = Task.query.get(id)
                print("task ", s.name)
                t.set_subtask(s)

            db.session().add(t)
            db.session().commit()

    return redirect(url_for("tasks_index"))


@app.route("/update/<task_id>/", methods=["GET", "POST"])
@login_required
def tasks_update(task_id):
    if current_user.admin:
        task = Task.query.get(task_id)
        all_categories = Category.query.all()
        old_categories = Category.query.join(tags).join(Task). \
            filter((tags.c.category_id == Category.id) & (tags.c.task_id == task_id)).all()

        if request.method == "GET":
            return render_template("tasks/updateform.html",
                                   form=TaskForm(),
                                   task=task,
                                   categories=all_categories,
                                   tags=old_categories)

        form = TaskForm(request.form)

        # TODO: validointi
        # if not form.validate():
        #   return render_template("tasks/update.html", form=form,
        #   task=task, categories=categories, tags=old_categories)

        t = Task.query.get(task_id)
        t.name = form.name.data
        t.description = form.description.data

        updated_categories = form.categories.data

        for c in all_categories:
            if str(c.id) in updated_categories and c not in old_categories:
                c.taskstagged.append(t)
            elif str(c.id) not in updated_categories and c in old_categories:
                c.taskstagged.remove(t)
            db.session.add(c)

        db.session().commit()
    return redirect(url_for("tasks_index"))


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
    db.session().commit()

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
    db.session().commit()

    return redirect(url_for("tasks_index"))
