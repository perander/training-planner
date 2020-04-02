from application import db
from application.models import Base

from sqlalchemy.sql import text


class Task(Base):
    __tablename__ = 'task'

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @staticmethod
    def show_tasksdone_in_order_of_popularity():
        stmt = text("SELECT task_id, task.name, COUNT(*)"
                    " FROM tasksdone, task"
                    " WHERE tasksdone.task_id = task.id"
                    " GROUP BY task_id"
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
                    " GROUP BY task_id"
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

tags = db.Table('tags',
                db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                )
