# coding=utf-8

from db_connect import db


class MessageType(db.Model):
    __tablename__ = 'message_type'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String(1500))
    messages=db.relationship('Message',backref='message_type',lazy='dynamic')


    def __init__(self, content):
        self.content = content


def create_table():
    db.create_all()


def insert_default_value():
    insert = MessageType(content='关注')
    db.session.add(insert)
    db.session.commit()
    
    insert2 = MessageType(content='帖子点赞')
    db.session.add(insert2)
    db.session.commit()

    insert3 = MessageType(content='回帖')
    db.session.add(insert3)
    db.session.commit()


    insert4 = MessageType(content='回复')
    db.session.add(insert4)
    db.session.commit()