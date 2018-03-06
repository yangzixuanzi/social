# -*-coding=utf-8-*-
from sqlalchemy import desc
from db_connect import db
from modules.Logger import *
import constant


# 用户认证


class IdentityAuthen(db.Model):
    __tablename__ = 'identity_authen'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=False, )
    identity_pre_img = db.Column(db.String(500), unique=False)  # 身份证
    employee_card_img = db.Column(db.String(500), unique=False)  # 工牌照片
    check_status = db.Column(db.Integer, unique=False)  # 审核状态 1.审核中 2.审核成功 3.审核不通过
    auth_type = db.Column(db.Integer, unique=False)  # 认证类别 1.实名认证 2.理财师认证
    check_idea = db.Column(db.String(500), unique=False)  # 审核意见
    create_time = db.Column(db.DateTime, unique=False)  # 创建时间
    check_time = db.Column(db.DateTime, unique=False, default=None)  # 审核时间

    def __init__(self, user_id, identity_pre_img, employee_card_img, check_status, auth_type, check_idea, create_time,
                 check_time):
        self.user_id = user_id
        self.identity_pre_img = identity_pre_img
        self.employee_card_img = employee_card_img
        self.check_status = check_status
        self.auth_type = auth_type
        self.create_time = create_time
        self.check_time = check_time
        self.check_idea = check_idea


def create_table():
    db.create_all()


def insert(user_id, identity_pre_img, employee_card_img, auth_type, create_time, check_time=None,
           check_status=constant.const.CHECK_STATUS_ONCHECK,check_idea=None):
    insert = IdentityAuthen(user_id=user_id, identity_pre_img=identity_pre_img, employee_card_img=employee_card_img,
                            check_status=check_status, auth_type=auth_type, check_idea=check_idea,
                            create_time=create_time, check_time=check_time)
    db.session.add(insert)
    db.session.commit()
    return insert


#  查询审核进度
def select_by_user_and_auth_type(user_id, auth_type):
    data = IdentityAuthen.query.filter(IdentityAuthen.user_id == user_id,
                                       IdentityAuthen.auth_type == auth_type).order_by(
        desc(IdentityAuthen.create_time)).first()
    return data


def select_by_user(user_id):
    data = IdentityAuthen.query.filter(IdentityAuthen.user_id == user_id,
                                       IdentityAuthen.check_status == constant.const.CHECK_STATUS_CHECK_PASS).order_by(
        desc(IdentityAuthen.auth_type)).first()
    return data


def update(auth):
    row = IdentityAuthen.query.get(auth.id)
    row.identity_pre_img = auth.identity_pre_img
    row.employee_card_img = auth.employee_card_img
    row.create_time = auth.create_time
    row.check_status = auth.check_status


def to_json(object):
    if isinstance(object, IdentityAuthen):
        return {
            'id': object.id,
            'user_id': object.user_id,
            'identity_pre_img': object.identity_pre_img,
            'employee_card_img': object.employee_card_img,
            'check_status': object.check_status,
            'auth_type': object.auth_type,
            'check_idea': object.check_idea,
            'create_time': object.create_time,
            'check_time': object.check_time
        }