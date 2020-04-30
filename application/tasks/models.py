from application import db
from application.models import Base
from application.category.models import Category, get_all_categories

from sqlalchemy.sql import text


class Subtask(db.Model):
    __tablename__ = 'subtask'
    supertask_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    subtask_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)


tags = db.Table('tags',
                db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                )


class Task(Base):
    __tablename__ = 'task'

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    tags = db.relationship('Category',
                           secondary=tags,
                           backref=db.backref('taggedtasks', lazy='dynamic'),
                           lazy='dynamic')
    # cascade='all, delete-orphan')

    supertasks = db.relationship('Subtask',
                                 foreign_keys=[Subtask.subtask_id],
                                 backref=db.backref('subtask', lazy='joined'),
                                 lazy='dynamic',
                                 cascade='all, delete-orphan')
    subtasks = db.relationship('Subtask',
                               foreign_keys=[Subtask.supertask_id],
                               backref=db.backref('supertask', lazy='joined'),
                               lazy='select',
                               cascade='all, delete-orphan')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def add_tag(self, category):
        self.tags.append(category)

    def remove_tag(self, category):
        self.tags.remove(category)

    def is_tag_for(self, task):
        if task.id is None:
            return False
        return self in task.tags.all()

    def get_tags(self):
        return Category.query.join(tags).join(Task).filter(
            (tags.c.category_id == Category.id) & (tags.c.task_id == self.id)).all()

    # in the next 4 methods, self refers to the task being created/updated.
    # A task can assign subtasks for itself, but not assign itself (as a subtask) for other tasks
    def set_subtask(self, task):
        if not task.has_supertask(self):
            s = Subtask(supertask=self, subtask=task)
            db.session.add(s)

    def remove_subtask(self, task):
        s = self.subtasks.filter_by(subtask_id=task.id).first()
        if s:
            db.session.delete(s)

    def has_subtask(self, task):
        if task.id is None:
            return False
        return self.subtasks.filter_by(
            subtask_id=task.id).first() is not None

    def has_supertask(self, task):
        if task.id is None:
            return False
        return self.supertasks.filter_by(
            supertask_id=task.id).first() is not None

    def get_subtasks(self):
        return [item.subtask for item in self.subtasks]

    @staticmethod
    def show_tasksinprogress_by(user):
        stmt = text("SELECT task_id, task.name, task.date_modified"
                    " FROM tasksinprogress, task"
                    " WHERE tasksinprogress.task_id = task.id"
                    " AND tasksinprogress.account_id = " + str(user.id) +
                    " GROUP BY task_id, task.name, task.date_modified "
                    " ORDER BY task.date_modified DESC")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1]})

        return response

    @staticmethod
    def show_tasksdone_in_order_of_popularity():
        stmt = text("SELECT task_id, task.name, COUNT(*)"
                    " FROM tasksdone, task"
                    " WHERE tasksdone.task_id = task.id"
                    " GROUP BY task_id, task.name"
                    " ORDER BY COUNT(*) DESC"
                    " LIMIT 5")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1], "done_by": row[2]})

        return response

    @staticmethod
    def show_tasksinprogress_in_order_of_popularity():
        stmt = text("SELECT task_id, task.name, COUNT(*)"
                    " FROM tasksinprogress, task"
                    " WHERE tasksinprogress.task_id = task.id"
                    " GROUP BY task_id, task.name"
                    " ORDER BY COUNT(*) DESC"
                    " LIMIT 5")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1], "inprogress_by": row[2]})

        return response


def exists(name):
    return Task.query.filter_by(name=name).first() is not None


def exists_another(task_id, name):
    for task in Task.query.filter_by(name=name).all():
        if task.id != int(task_id):
            return True
    return False


def find(task_id):
    return Task.query.get(task_id)


def get_all_tasks():
    return Task.query.all()


def all_tasks_ordered_by_createdate():
    return Task.query.order_by(Task.date_created.desc())


def create(name, description, categories, subtasks):
    t = Task(name, description)

    for id in categories:
        c = Category.query.get(id)
        t.add_tag(c)

    for id in subtasks:
        s = Task.query.get(id)
        t.set_subtask(s)

    db.session().add(t)


def update(task_id, name, description, categories, subtasks):
    task = find(task_id)
    task.name = name
    task.description = description

    all_categories = get_all_categories()
    all_subtasks = get_all_tasks()

    old_categories = task.get_tags()
    old_subtasks = task.get_subtasks()

    updated_categories = categories
    updated_subtasks = subtasks

    for c in all_categories:
        if str(c.id) in updated_categories and c not in old_categories:
            task.add_tag(c)
        elif str(c.id) not in updated_categories and c in old_categories:
            task.remove_tag(c)

    for st in all_subtasks:
        if str(st.id) in updated_subtasks and st not in old_subtasks:
            task.set_subtask(st)
        elif str(st.id) not in updated_subtasks and st in old_subtasks:
            task.remove_subtask(st)

    db.session.add(task)


def delete(task_id):
    t = Task.query.get(task_id)
    db.session().delete(t)


done = db.Table('tasksdone',
                db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
                db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                )

inprogress = db.Table('tasksinprogress',
                      db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
                      db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                      )
