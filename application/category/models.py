from application import db
from application.models import Base
from application.tasks.models import tags


class Category(Base):
    __tablename__ = 'category'

    name = db.Column(db.String(144), nullable=False)

    # (maybe) description = db.Column(db.String(200), nullable=False)

    taskstagged = db.relationship('Task',
                                  secondary=tags,
                                  backref=db.backref('taggedwith',
                                                     lazy='dynamic'),
                                  lazy='dynamic')

    def __init__(self, name):
        self.name = name
