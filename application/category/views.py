from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.category.models import Category, create, exists, exists_another, delete, get_all_categories, find, \
    update, all_categories_ordered_by_createdate
from application.category.forms import CategoryForm


@app.route("/categories", methods=["GET"])
def categories_index():
    page = request.args.get('page', 1, type=int)
    pagination = all_categories_ordered_by_createdate().paginate(page, per_page=10)
    categories = pagination.items

    return render_template("categories/list.html", categories=categories, pagination=pagination)


@app.route("/categories/<category_id>/")
def categories_view(category_id):
    c = find(category_id)
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


@app.route("/update/<category_id>", methods=["GET", "POST"])
@login_required(role="ADMIN")
def categories_update(category_id):
    category = find(category_id)

    if request.method == "GET":
        return render_template("categories/updateform.html",
                               form=CategoryForm(),
                               category=category)

    form = CategoryForm(request.form)

    if form.validate():
        if exists_another(category_id, form.name.data):
            return render_template("categories/updateform.html",
                                   form=CategoryForm(),
                                   category=category,
                                   error="Category " + form.name.data + " already exists")

        update(category_id, form.name.data)

    db.session().commit()
    return redirect(url_for("categories_index"))


@app.route("/deletecategory/<category_id>", methods=["POST"])
@login_required(role="ADMIN")
def categories_delete(category_id):
    delete(category_id)
    db.session().commit()

    return redirect(url_for("categories_index"))
