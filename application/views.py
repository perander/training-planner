from flask import render_template, request, redirect, url_for
from flask_login import current_user
from application import app, login_required
from application.category.models import Category
from application.tasks.models import Task
from sqlalchemy import func

@app.route("/")
@login_required
def index():
    if current_user.admin:
        return redirect(url_for("tasks_index"))

    # TODO: new tasks per user
    # new = Task.show_new_tasks(current_user)
    new = Task.query.all()
    inprogress = Task.show_tasksinprogress_by(current_user)
    return render_template("index.html",
                           new=new,
                           inprogress=inprogress)


@app.route("/", methods=["POST"])
def search():
    query = func.lower(request.form.get("query"))

    foundtasks = Task.query.filter(func.lower(Task.name).contains(query)).all()
    foundcategories = Category.query.filter(func.lower(Category.name).contains(query)).all()

    if (foundtasks is None or len(foundtasks) == 0) and \
            (foundcategories is None or len(foundcategories) == 0):
        return render_template("notfound.html")

    return render_template("found.html", foundtasks=foundtasks,
                           foundcategories=foundcategories)
