from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.category.models import *
from application.category.forms import CategoryForm


@app.route("/categories", methods=["GET"])
def categories_index():
    return render_template("categories/list.html", categories=Category.query.all())


@app.route("/categories/<category_id>/")
def categories_view(category_id):
    c = Category.query.get(category_id)
    tasks = c.taggedtasks.all()
    return render_template("categories/view.html", category=c, tasks=tasks)


@app.route("/categories/new", methods=["GET", "POST"])
@login_required(role="ADMIN")
def categories_create():
    if request.method == "GET":
        return render_template("categories/new.html", form=CategoryForm())

    form = CategoryForm(request.form)

    if not form.validate():
        return render_template("categories/new.html", form=form)

    if exists(form.name.data):
        return render_template("categories/new.html", form=form,
                               error="Category already exists")

    create(form.name.data)
    db.session().commit()

    return redirect(url_for("categories_index"))


@app.route("/deletecategory/<category_id>", methods=["POST"])
@login_required(role="ADMIN")
def categories_delete(category_id):
    delete(category_id)
    db.session().commit()

    return redirect(url_for("categories_index"))
