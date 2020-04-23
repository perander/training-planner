from application import db
from application.models import Base
from application.category.models import Category

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
                               lazy='dynamic',
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

    # in these 4 methods, self refers to the task being created/updated.
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

    # @staticmethod
    # def show_new_tasks(user):
    #     stmt = text("SELECT task.id, tasksinprogress.task_id,"
    #                 "tasksdone.task_id, tasksinprogress.account_id, "
    #                 "tasksdone.account_id, task.name "
    #                 " FROM tasksinprogress, task, account"
    #                 " WHERE tasksinprogress.task_id = task.id"
    #                 " AND tasksinprogress.account_id = " + str(user.id) +
    #                 " GROUP BY task_id, task.name"
    #                 " ORDER BY task.date_modified DESC")
    #
    #     res = db.engine.execute(stmt)
    #
    #     response = []
    #     for row in res:
    #         response.append({"id": row[0], "name": row[1], "date": row[2]})
    #
    #     return response

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
                    " ORDER BY COUNT(*) DESC")

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
                    " ORDER BY COUNT(*) DESC")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1], "inprogress_by": row[2]})

        return response


done = db.Table('tasksdone',
                db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
                db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                )

inprogress = db.Table('tasksinprogress',
                      db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
                      db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                      )
