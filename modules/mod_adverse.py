# coding=utf-8
import requests
from flask import session

import constant
from Logger import *


def pay_adverse(request):
    Logger().logger.info('now do pay adverse !')
    result = {'code': 0, 'message': 'success'}
    adverse_contract_id = request.args.get('adverseId')
    ip = request.remote_addr
    url = request.args.get('url')
    search = request.args.get('search')
    params = {'ip': ip, 'url': url, 'adverseContractId': adverse_contract_id,'triggerQuery': search}
    if session.get('userinfo'):
        params['userId'] = session.get('userinfo')['id']
        params['userName'] = session.get('userinfo')['name']
    headers = {'content-type': 'application/json'}
    response = requests.post(constant.const.ADVERSE_PAYMENT_URL, json=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['code'] != 0:
            result = {'code': 1, 'message': 'pay adverse fail !'}
    Logger().logger.info('code:%s,message:%s', result['code'], result['message'])
    return result


def find_adverse(request):
    Logger().logger.info('now do pay adverse !')
    title = request.args.get("name")
    result_num = 4
    params = {'query': title, 'type': 'search_social', 'result_num': result_num}
    response = requests.get(constant.const.ADVERSE_MATCHED_ADVERSE_URL, params=params)
    return response
