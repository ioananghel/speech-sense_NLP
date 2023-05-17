# import db from this package
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# database models for users and notes(in this case)
# articles on google average at around 2000 words, at around 5 chars per word
# safe to assume that the average article has around 10 000 chars
# to be somewhat safe, for this proof of concept 10 times that should be good enough
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    content = db.Column(db.String(10000))
    sentiment = db.Column(db.String(1000))

# one User to many Notes
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # you can access all of the notes of a user from this notes vector