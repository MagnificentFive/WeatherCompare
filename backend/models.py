from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.String(100))
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    image_url = db.Column(db.Text)
