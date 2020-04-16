from application import db
from application.models import Base


class Category(Base):
    __tablename__ = 'category'

    name = db.Column(db.String(144), nullable=False)

    def __init__(self, name):
        self.name = "#" + name

    def __str__(self):
        return self.name
