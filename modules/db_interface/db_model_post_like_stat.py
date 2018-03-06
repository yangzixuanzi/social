# coding=utf-8
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from db_connect import db
from modules.Logger import *


class PostLikeActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, unique=False)
    create_time = db.Column(db.DateTime, unique=False)
    status=db.Column(db.Boolean, unique=False, default=0)

    def __init__(self, post_id, user_id, create_time,status):
        self.post_id = post_id
        self.user_id = user_id
        self.create_time = create_time
        self.status = status


def create_table():
    db.create_all()


def is_post_liked_by_user(post_id, user_id):
    Logger().logger.info('post_id:%s,user_id:%s',post_id, user_id)
    count = PostLikeActivity.query.filter_by(post_id=post_id, user_id=user_id, status=True).count()
    return count > 0


def insert_or_update(post_id, user_id, create_time, status):
    data = PostLikeActivity.query.filter_by(post_id=post_id, user_id=user_id).first()
    if data:
        data.status = status
        data.create_time = create_time
    else:
        insert = PostLikeActivity(post_id=post_id, user_id=user_id, create_time=create_time, status=status)
        db.session.add(insert)
    db.session.commit()


