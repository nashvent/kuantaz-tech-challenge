from config import ma
from models import Project, Institution, User
from marshmallow import fields

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