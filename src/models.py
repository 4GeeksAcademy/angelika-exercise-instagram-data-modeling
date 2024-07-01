import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    fullname = Column(String(250), nullable=False)
    bio = Column(String(250))
    profile_image = Column(String(250))
    created_at = Column(DateTime, nullable=False)

    posts = relationship('Post', backref='author', lazy=True)
    comments = relationship('Comment', backref='author', lazy=True)
    likes = relationship('Like', backref='user', lazy=True)
    followers = relationship('Follow', foreign_keys='Follow.user_to_id', backref='followed', lazy='dynamic')
    following = relationship('Follow', foreign_keys='Follow.user_from_id', backref='follower', lazy='dynamic')

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    image_url = Column(String(250))
    caption = Column(String(500))
    created_at = Column(DateTime, nullable=False)

    comments = relationship('Comment', backref='post', lazy=True)
    likes = relationship('Like', backref='post', lazy=True)

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    created_at = Column(DateTime, nullable=False)

class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    created_at = Column(DateTime, nullable=False)

class Follow(Base):
    __tablename__ = 'follow'

    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'))
    user_to_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, nullable=False)

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
