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
    

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
