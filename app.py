from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nash:123456@localhost:5432/kuantaz'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'p4CxcSbRn9PFZuxKksQI'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    projects = db.relationship('Project', backref='institution', lazy=True)
    def __init__(self, name):
        self.name = name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    rut = db.Column(db.String(15), nullable=False)
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

class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_fk = True
        fields = ("id", "name")

class InstitutionSchema(ma.Schema):
    class Meta:
        model = Institution
        fields = ("id", "name", "projects")
    projects = fields.Nested(ProjectSchema, many=True)
    
class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "name", "projects")
    projects = fields.Nested(ProjectSchema, many=True)


@app.route("/")
def hello_kuantaz():
    return "<p>Hello, Kuantaz!</p>"
  
@app.route("/institution")
def list_institutions():
    institutions = Institution.query.all()
    institution_schema = InstitutionSchema(many=True)
    return institution_schema.dump(institutions)

@app.route("/user")
def list_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)



if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
