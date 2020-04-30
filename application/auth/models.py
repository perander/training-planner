from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from application import db, bcrypt
from application.tasks.models import done, inprogress
from application.models import Base
from application.tasks.models import Task, find, get_all_tasks


class User(Base):
    __tablename__ = 'account'

    username = db.Column(db.String(144), nullable=False, unique=True)
    _password = db.Column(db.String(144), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    # todo: cascade all, delete-orphan -> pitäisi toimia niin että deletoi
    # association tablesta, ei taskeista tai accountista
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
        self._password = bcrypt.generate_password_hash(plaintext) \
            .decode('utf-8')  # for heroku

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

    def roles(self):
        if self.admin:
            return ["ADMIN"]
        return []

    def mark_done(self, task_id):
        task = find(task_id)

        self.tasksdone.append(task)
        if task in self.tasksinprogress:
            self.tasksinprogress.remove(task)

        db.session().add(self)

    def mark_inprogress(self, task_id):
        task = find(task_id)
        self.tasksinprogress.append(task)
        db.session().add(self)

    def get_new_tasks(self):
        tasks = get_all_tasks()
        new = []

        for task in tasks:
            if task not in self.tasksdone and task not in self.tasksinprogress:
                new.append(task)

        return new

    def recommendations(self):
        tasks = self.get_new_tasks()

        recommended = []

        for task in tasks:
            goal = len(task.subtasks)
            found = 0
            for d in self.tasksdone:
                if d.id != task.id and d.has_supertask(task):
                    found += 1
            if found == goal:
                recommended.append(task)

        return recommended
