from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required

from application.tasks.models import Task, tags, find, \
    get_all_tasks, exists, exists_another, create, update, delete, all_tasks_ordered_by_createdate
from application.tasks.forms import TaskForm

from application.auth.models import User

from application.category.models import Category, get_all_categories, all_categories_ordered_by_createdate


@app.route("/tasks", methods=["GET"])
def tasks_index():
    page = request.args.get('page', 1, type=int)
    pagination = all_tasks_ordered_by_createdate().paginate(page, per_page=8)
    tasks = pagination.items

    return render_template("tasks/list.html", tasks=tasks, pagination=pagination)


@app.route("/tasks/<task_id>/")
def tasks_view(task_id):
    task = find(task_id)
    return render_template("tasks/view.html", task=task,
                           categories=task.get_tags(), subtasks=task.get_subtasks())


@app.route("/tasks/new", methods=["GET", "POST"])
@login_required(role="ADMIN")
def tasks_create():
    categories = get_all_categories()
    tasks = get_all_tasks()

    if request.method == "GET":
        return render_template("tasks/new.html", form=TaskForm(),
                               categories=categories, tasks=tasks)

    form = TaskForm(request.form)

    # TODO: multipleselectfield doesn't support form.validate, need custom validation
    # if not form.validate():
    #    return render_template("tasks/new.html", form=form)

    if form.is_submitted() and exists(form.name.data):
        return render_template("tasks/new.html", form=form,
                               categories=categories,
                               tasks=tasks,
                               error="Task " + form.name.data + " already exists")

    create(form.name.data,
           form.description.data,
           form.categories.data,
           form.subtasks.data)

    db.session().commit()

    return redirect(url_for("tasks_index"))


@app.route("/update/<task_id>/", methods=["GET", "POST"])
@login_required(role="ADMIN")
def tasks_update(task_id):
    task = find(task_id)

    if request.method == "GET":
        return render_template("tasks/updateform.html",
                               form=TaskForm(),
                               task=task,
                               categories=get_all_categories(),
                               tags=task.get_tags(),
                               subtasks=get_all_tasks(),
                               existing=task.get_subtasks()
                               )

    form = TaskForm(request.form)

    # TODO: validointi
    # if not form.validate():
    #   return render_template("tasks/update.html", form=form,
    #   task=task, categories=categories, tags=old_categories)

    if exists_another(task_id, form.name.data):
        return render_template("tasks/updateform.html",
                               form=form,
                               task=task,
                               categories=get_all_categories(),
                               tags=task.get_tags(),
                               subtasks=get_all_tasks(),
                               existing=task.get_subtasks(),
                               error="Task " + form.name.data + " already exists")

    update(task_id,
           form.name.data,
           form.description.data,
           form.categories.data,
           form.subtasks.data)

    db.session().commit()
    return redirect(url_for("tasks_index"))


@app.route("/deletetask/<task_id>", methods=["POST"])
@login_required(role="ADMIN")
def tasks_delete(task_id):
    delete(task_id)
    db.session().commit()
    return redirect(url_for("tasks_index"))


@app.route("/setdone/<task_id>/", methods=["POST"])
@login_required
def tasks_set_done(task_id):
    if current_user.admin:
        return redirect(url_for("tasks_index"))

    current_user.mark_done(task_id)
    db.session().commit()

    return redirect(url_for("tasks_view", task_id=task_id))


@app.route("/setinprogress/<task_id>/", methods=["POST"])
@login_required
def tasks_set_inprogress(task_id):
    if current_user.admin:
        return redirect(url_for("tasks_index"))

    current_user.mark_inprogress(task_id)
    db.session().commit()

    return redirect(url_for("tasks_view", task_id=task_id))
