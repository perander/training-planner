from application import db
from application.models import Base


class Task(Base):
    __tablename__ = 'task'

    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description


done = db.Table('tasksdone',
                db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
                db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                )

inprogress = db.Table('tasksinprogress',
                      db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
                      db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                      )

tags = db.Table('taskscategory',
                db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
                )
