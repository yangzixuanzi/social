# coding=utf-8
import re

from flask import session

import constant
from Logger import *
from db_interface import db_model_user


def service(request):
    if request.method == 'POST':
        operate_type = request.form.get("type")
        if operate_type == 'check_exist':
            mobile = request.form.get("mobile")
            return check_exist(mobile)
        elif operate_type == 'create':
            return register_check(request)


#  验证手机号格式
def check_mobile(mobile):
    Logger().logger.info('now do check_mobile  phone:'+mobile)
    p = re.compile('^1(3|4|5|7|8)\d{9}$')
    result = {}
    match = p.match(mobile)
    if match:
        result['code'] = 0
        result['message'] = '手机号码格式验证通过'
    else:
        result['code'] = 1
        result['message'] = '手机号码格式错误'
    return result


# 检查手机号码是否存在
def check_exist(mobile):
    result = {}
    user = db_model_user.select_by_mobile(mobile)
    if user:
        result['code'] = 1
        result['message'] = '手机号已存在!'
    else:
        result['code'] = 0
        result['message'] = '手机号不存在!'
    return result


# 注册验证
def register_check(request):
    mobile = request.form.get("mobile")
    sms_code = request.form['sms_code']
    result = {}
    check_mobile_result = check_mobile(mobile)
    if check_mobile_result['code'] != 0:
        result['code'] = 1
        result['message']=check_mobile_result['message']
        return result

    check_exist_result = check_exist(mobile)
    if check_exist_result['code'] != 0:
        result['code'] = 2
        result['message'] = check_exist_result['message']
        return result
    if not session['sms_code'] or session['sms_code']['phone'] != mobile:
        result['code'] = 3
        result['message'] = '尚未生成验证码!'
        return result
    create_time = session['sms_code']['create_time']
    now_time = time.time()
    cha = now_time - create_time
    if cha <= constant.const.SEND_SMS_CODE_TIME:
        if sms_code == session['sms_code']['code']:
            result['code'] = 0
            result['message'] = '注册验证通过!'
            session['userinfo'] = {'mobile': mobile}
            session['sms_code'] = None
            Logger().logger.info('mobile:%s,result:%s',mobile,result)
        else:
            result['code'] = 4
            result['message'] = '验证码不正确!'
    else:
        result['code'] = 5
        result['message'] = '验证码过期!'
        session['sms_code'] = None
    Logger().logger.error('result:%s', result)
    return result
