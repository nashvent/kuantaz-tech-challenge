from flask import request
from datetime import datetime, date

from config import app, db
from models import Institution, User, Project
from schema import UserSchema, InstitutionSchema, ProjectSchema, ProjectDetailSchema, InstitutionDetailSchema, ProjectSummarySchema

@app.route("/")
def hello_kuantaz():
    return "<p>Hello, Kuantaz!</p>"

@app.route("/institution", methods = ['GET','POST'])
def list_create_institutions():
    if request.method == 'GET':
      institutions = Institution.query.all()
      return InstitutionSchema(many=True, exclude=['projects']).dump(institutions)
    
    if request.method == 'POST':
      name = request.json.get('name', 'without name')
      description = request.json.get('description', 'without description')
      address = request.json.get('address', 'without address')
      institution = Institution(name, description, address)
      db.session.add(institution)
      db.session.commit()
      return InstitutionSchema(exclude=['projects']).dump(institution)

@app.route("/institution/<id>", methods = ['GET','PUT','DELETE'])
def update_delete_institutions(id):
    if request.method == 'GET':
      institution = Institution.query.get(id)
      return InstitutionDetailSchema().dump(institution)
    
    if request.method == 'PUT':
      institution = Institution.query.get(id)
      institution.name = request.json.get('name', 'without name')
      institution.description = request.json.get('description', 'without description')
      institution.address = request.json.get('address', 'without address')
      db.session.commit()
      return InstitutionSchema().dump(institution)
    
    if request.method == 'DELETE':
      institution = Institution.query.get(id)
      db.session.delete(institution)
      db.session.commit()
      return InstitutionSchema().dump(institution)

      
@app.route("/user", methods = ['GET','POST'])
def list_create_users():
    if request.method == 'GET':
      users = User.query.all()
      return UserSchema(many=True, exclude=['projects']).dump(users)
    
    if request.method == 'POST':
      name = request.json.get('name', 'default name')
      lastname = request.json.get('lastname', 'default lastname')
      rut = request.json.get('rut')
      born_date = request.json.get('born_date', date(1900,1,1))
      if( isinstance(born_date, date) == False ):
        born_date = datetime.strptime(born_date, '%d-%m-%Y').date()
      role = request.json.get('role')
      user = User(name, lastname, rut, born_date, role)
      db.session.add(user)
      db.session.commit()
      return UserSchema().dump(user)
      
@app.route("/user/<rut>", methods = ['GET'])
def get_user(rut):
    if request.method == 'GET':
      user = User.query.filter_by(rut=rut).first()
      return UserSchema().dump(user)
    
    
@app.route("/project", methods = ['GET','POST'])
def list_create_projects():
    if request.method == 'GET':
      projects = Project.query.all()
      return ProjectSchema(many=True).dump(projects)
    
    if request.method == 'POST':
      name = request.json.get('name', 'default name')
      description = request.json.get('description', 'default description')
      start_date = request.json.get('start_date', date.today())
      if( isinstance(start_date, date) == False ):
        start_date = datetime.strptime(start_date, '%d-%m-%Y').date()
      end_date = request.json.get('end_date', date.today())
      if( isinstance(end_date, date) == False ):
        end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
      institution_id = request.json.get('institution_id')
      user_id = request.json.get('user_id')
      
      project = Project(name, description, start_date, end_date, institution_id, user_id)
      db.session.add(project)
      db.session.commit()
      return ProjectSchema().dump(project)
      
@app.route("/project/<id>", methods = ['GET'])
def get_project(id):
    if request.method == 'GET':
      project = Project.query.get(id)
      return ProjectDetailSchema().dump(project)

@app.route("/project/summary", methods = ['GET'])
def list_projects_summary():
    if request.method == 'GET':
      projects = Project.query.all()
      return ProjectSummarySchema(many=True).dump(projects)

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
