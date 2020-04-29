from application import db
from application.models import Base


class Category(Base):
    __tablename__ = 'category'

    name = db.Column(db.String(144), nullable=False)

    def __init__(self, name):
        self.name = "#" + name

    def __str__(self):
        return self.name


def exists(name):
    return Category.query.filter_by(name='#' + name).first() is not None


def find(category_id):
    return Category.query.get(category_id)


def create(name):
    c = Category(name)
    db.session().add(c)


def get_all_categories():
    return Category.query.all()


def delete(category_id):
    c = Category.query.get(category_id)
    db.session().delete(c)
