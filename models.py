from config import db

class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    projects = db.relationship('Project', backref='institution', lazy=True)
    def __init__(self, name, description, address):
        self.name = name
        self.description = description
        self.address = address


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    rut = db.Column(db.String(15), nullable=False, unique=True)
    born_date = db.Column(db.Date)
    role = db.Column(db.String(100))
    projects = db.relationship('Project', backref='user', lazy=True)
    def __init__(self, name, lastname, rut, born_date, role):
        self.name = name
        self.lastname = lastname
        self.rut = rut
        self.born_date = born_date
        self.role = role
    

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship('User', uselist=False, lazy='select')
    def __init__(self, name, description, start_date, end_date, institution_id, user_id):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.institution_id = institution_id
        self.user_id = user_id
