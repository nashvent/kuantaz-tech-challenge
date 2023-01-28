from flask import request
from config import app, db
from models import Institution, User
from schema import UserSchema, InstitutionSchema

@app.route("/")
def hello_kuantaz():
    return "<p>Hello, Kuantaz!</p>"

institution_schema = InstitutionSchema()
institutions_schema = InstitutionSchema(many=True)

@app.route("/institution", methods = ['GET','POST'])
def list_create_institutions():
    if request.method == 'GET':
      institutions = Institution.query.all()
      return institutions_schema.dump(institutions)
    if request.method == 'POST':
      name = request.json.get('name', 'without name')
      description = request.json.get('description', 'without description')
      address = request.json.get('address', 'without address')
      institution = Institution(name, description, address)
      db.session.add(institution)
      db.session.commit()
      return institution_schema.dump(institution)

@app.route("/institution/<id>", methods = ['GET','PUT','DELETE'])
def update_delete_institutions(id):
    if request.method == 'GET':
      institution = Institution.query.get(id)
      return institution_schema.dump(institution)
    
    if request.method == 'PUT':
      institution = Institution.query.get(id)
      institution.name = request.json.get('name', 'without name')
      institution.description = request.json.get('description', 'without description')
      institution.address = request.json.get('address', 'without address')
      db.session.commit()
      return institution_schema.dump(institution)
    
    if request.method == 'DELETE':
      institution = Institution.query.get(id)
      db.session.delete(institution)
      db.session.commit()
      return institution_schema.dump(institution)


      
@app.route("/user")
def list_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)


if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
