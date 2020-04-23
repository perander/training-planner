from flask import render_template
from flask_login import login_required

from application import app
from application.tasks.models import Task


@app.route("/stats")
@login_required
def stats():
    return render_template("stats/toplist.html",
                           topdone=Task.show_tasksdone_in_order_of_popularity(),
                           topinprogress=Task.show_tasksinprogress_in_order_of_popularity())
