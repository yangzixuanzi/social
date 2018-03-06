# coding=utf-8
import random

import requests
from flask import session

import constant
from Logger import *

default_sms_length = 6

# 发送手机验证码
def send_sms_code(request):
    phone = request.form.get('mobile')
    if not phone:
        result = {'code': 1, 'sms_code': '', "message": 'phone is none!'}
        return result
    code = create_phone_code()
    content = '尊敬的用户您好，本次的验证码为:' + code
    params = {'phones': phone, 'content': content}
    headers = {'content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
    response = requests.post(constant.const.SEND_SMS_CODE, data=params, headers=headers)
    Logger().logger.info('phone:' + phone+' code'+code)
    if response.status_code == 200:
        result = {'code': 0, 'sms_code': code, "message": 'success'}
        session['sms_code'] = {'create_time': time.time(), 'code': code, 'phone': phone}
        Logger().logger.info('send sms code success!')
    else:
        result = {'code': 1, 'sms_code': code, "messgae": 'send sms_code'}
        Logger().logger.info('send sms code fail!')
    return result


def create_phone_code():
    chars = ['0','1','2','3','4','5','6','7','8','9']
    code_sms=[]
    random.seed()
    for i in range(default_sms_length):
        code_sms.append(random.choice(chars))
    verifyCode = "".join(code_sms)
    Logger().logger.info('sms verifyCode:' + verifyCode)
    return verifyCode
