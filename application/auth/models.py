from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from application import db, bcrypt
from application.tasks.models import done, inprogress


class User(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    username = db.Column(db.String(144), nullable=False, unique=True)
    _password = db.Column(db.String(144), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    tasksdone = db.relationship('Task',
                                secondary=done,
                                backref=db.backref('doneby',
                                                   lazy='dynamic'),
                                lazy='dynamic')

    tasksinprogress = db.relationship('Task',
                                      secondary=inprogress,
                                      backref=db.backref('inprogressby',
                                                         lazy='dynamic'),
                                      lazy='dynamic')

    def __init__(self, username, plaintext, admin):
        self.username = username
        self.password = plaintext  # redirects to the method password(self, plaintext)
        self.admin = admin

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    @hybrid_method
    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
