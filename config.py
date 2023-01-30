from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nash:123456@localhost:5432/kuantaz'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'p4CxcSbRn9PFZuxKksQI'
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
