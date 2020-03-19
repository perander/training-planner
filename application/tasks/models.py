from application import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    inprogress = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String(144), nullable=False)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.done = False
        self.inprogress = False
