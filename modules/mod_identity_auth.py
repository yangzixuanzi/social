# coding=utf-8
from flask import session

import constant
import mod_base64
from Logger import *
from db_interface import db_model_identity_authentication


def service(request):
    if request.method == 'POST':
        return user_authentication(request)
    else:
        return query_user_auth()


# 1.个人认证 提交 身份证正面照
# 2.理财师认证 提交  a:已通过个人认证的，只提交工牌照片，未通过或者未认证的都提交
def user_authentication(request):
    auth_type = int(request.form.get('auth_type'));
    if not session.get('userinfo'):
        result = {'code': 1, 'message': 'user not login !'}
        return result
    user_id = session.get('userinfo')['id']
    path_type = 'identity'
    employee_card_img = None
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    if auth_type == constant.const.AUTH_TYPE_PERSONAL:
        identity_pre_img = request.form.get('identity_pre_img')
        identity_pre_img = mod_base64.base64_to_imgurl(identity_pre_img, path_type)
    elif auth_type == constant.const.AUTH_TYPE_FINANCE_CONSULTANT:
        # 判断是否个人认证通过
        data = db_model_identity_authentication.select_by_user_and_auth_type(user_id, constant.const.AUTH_TYPE_PERSONAL)
        if data and data.check_status == constant.const.CHECK_STATUS_CHECK_PASS:
            identity_pre_img = data.identity_pre_img
        else:
            identity_pre_img = request.form.get('identity_pre_img')
            identity_pre_img = mod_base64.base64_to_imgurl(identity_pre_img, path_type)
        employee_card_img = request.form.get('employee_card_img')
        employee_card_img = mod_base64.base64_to_imgurl(employee_card_img, path_type)
    data = db_model_identity_authentication.insert(user_id,identity_pre_img, employee_card_img,auth_type,create_time)
    Logger().logger.info('save identity_authentication'+str(db_model_identity_authentication.to_json(data)))
    result = {'code': 0, 'message': 'success !'}
    return result


# 查询 用户 认证信息
def query_user_auth():
    user_id = session.get('userinfo')['id']
    data_person = db_model_identity_authentication.select_by_user_and_auth_type(user_id,
                                                                                constant.const.AUTH_TYPE_PERSONAL)
    data_finance = db_model_identity_authentication.select_by_user_and_auth_type(user_id,
                                                                                 constant.const.AUTH_TYPE_FINANCE_CONSULTANT)
    data_person_status, data_finance_status = 0, 0
    if data_person:
        data_person_status = data_person.check_status
    if data_finance:
        data_finance_status = data_finance.check_status
    return data_person_status, data_finance_status



