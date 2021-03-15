from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Text, TIMESTAMP
import datetime
db = SQLAlchemy()


class User(db.Model):
    id = Column(Integer(), primary_key=True)
    username = Column(String(30))
    password = Column(String(8))


class Article(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    uid = Column(Integer())
    create_time = Column('create_time', TIMESTAMP, default=datetime.datetime.now)
