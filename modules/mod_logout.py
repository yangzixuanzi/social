from flask import session
from Logger import *


def service():
    result = {'succ': 1, 'code': 1, 'message': 'logout fail'}
    userinfo = session.get('userinfo')
    if userinfo is not None:
        session['userinfo'] = None
        session['sms_code'] = None
        result['succ'] = '0'
        result['code'] = '0'
        result['message'] = 'logout succ'
    Logger().logger.info('result code: %s ,message: %s', result['code'], result['message'])
    return result
