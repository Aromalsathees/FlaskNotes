from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()

# create user Model
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(200),nullable=False)
