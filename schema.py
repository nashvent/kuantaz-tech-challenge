from config import ma
from models import Project, Institution, User
from marshmallow import fields
from datetime import datetime

class ProjectSchema(ma.Schema):
    class Meta:
        ordered = True
        model = Project
        include_fk = True
        fields = ("id", "name", "description", "start_date", "end_date")

class InstitutionSchema(ma.Schema):
    class Meta:
        ordered = True
        model = Institution
        fields = ("id", "short_name", "name", "description", "address", "location", "created_at", "projects")
    projects = fields.Nested(ProjectSchema, many=True)
    location= fields.Function(lambda institution: f'“https://www.google.com/maps/search/{institution.address}')
    short_name = fields.Function(lambda institution: institution.name[:3])
    
class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        model = User
        fields = ("id", "name", "lastname", "rut", "born_date", "role", "projects", "age")
    projects = fields.Nested(ProjectSchema, many=True)
    born_date = fields.Function(lambda user: user.born_date.strftime('%d-%m-%Y'))
    age = fields.Function(lambda user: datetime.now().year - user.born_date.year)
    
    
class ProjectDetailSchema(ma.Schema):
    class Meta:
        ordered = True
        model = Project
        include_fk = True
        fields = ("id", "name", "description", "start_date", "end_date", "user", "institution")
    user = fields.Nested(UserSchema(exclude=['projects']))
    institution = fields.Nested(InstitutionSchema(exclude=['projects']))
        
class InstitutionDetailSchema(InstitutionSchema):
    projects = fields.Nested(ProjectDetailSchema(exclude=['institution']), many=True)
    
class ProjectSummarySchema(ma.Schema):
    class Meta:
        ordered = True
        model = Project
        fields = ("id", "name", "remaining_days")
    remaining_days = fields.Function(lambda project: (project.end_date - datetime.now()).days)