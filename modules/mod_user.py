# coding=utf-8
import json

from flask import session

import constant
import time_format
from Logger import *
from db_interface import db_model_action
from db_interface import db_model_action_type
from db_interface import db_model_community
from db_interface import db_model_message
from db_interface import db_model_post
from db_interface import db_model_user
from db_interface import db_model_user_relation

default_page_no = 1
default_num_perpage = 20
default_community_id = 0
default_post_id = 0
default_relation = 0
has_relation = 1
cancel_relation = 2
default_relation_id = 0
max_num_perpage = 100


def service(request):
    Logger().logger.info('enter user  service')
    if request.method == 'POST':
        type = request.form.get("type")
        if type == "create":
            return create_user(request)
        elif type == "modify":
            return modify_user_from_mobile(request)
        elif type == "check_user_name":
            return check_user_name(request)
        elif type == "modify_password":
            return modify_password(request)
        else:
            Logger().logger.error('error request:%s',request)
    elif request.method == 'GET':
            user_id = request.args.get("user_id")
            if user_id > 0:
                return query_user_info(user_id) ## 查询个人主页，
            else:
                return query_login_user_info()


def create_user(request):
    Logger().logger.info('now create new user ')
    # insert to db
    mobile = request.form.get("mobile")
    password = request.form.get("password")
    Logger().logger.info('password:%s,mobile:%s',password, mobile)
    Logger().logger.info('now insert to db')
    name = mobile.encode("utf-8")[0:3] + "****" + mobile[-4:]
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    db_model_user.insert(name=name, password=password, mobile=mobile,create_time=create_time)

    # return select value
    user = db_model_user.select_by_mobile(mobile=mobile)
    if user:
        Logger().logger.info('now update session info')
        if session['userinfo'] is None:
            Logger().logger.info('now create session info')
            session['userinfo'] = {'name': user.name, 'id': user.id}
        else:
            Logger().logger.info('now add session info')
            session['userinfo'] = {'mobile': mobile, 'name': user.name, 'id': user.id}
            Logger().logger.info('record action user regist:')
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        db_model_action.insert(user_id=user.id, \
                               action_type_id=db_model_action_type.get_type_id('regist'), action_detail_info='', \
                               create_time=create_time)
        Logger().logger.info('after create user,session is:%s', session)
        result = {'code': 0, 'message': 'create user succ!'}
    else:
        result = {'code': -1, 'message': 'create user fail!'}
        Logger().logger.error('result:%s', result)
    Logger().logger.info('result:%s', result)
    return result, user


def modify_user_from_mobile(request):
    Logger().logger.info('now modify  user info  from mobile')
    # insert to db
    result = {'succ': '1'}
    name = request.form.get("name")
    label = request.form.get("label")
    mobile = request.form.get("mobile")
    if name is None or label is None or mobile is None:
        result['code'] = '1'
        result['message'] = 'name or lable or mobile is null'
        Logger().logger.error('result:%s', result)
    else:
        user = db_model_user.select_by_mobile(mobile)
        if user:
            user.name = name
            user.label = label
            db_model_user.update_user(user)
            session['userinfo'] = {'mobile': mobile, 'name': user.name, 'id': user.id}
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'fill user info succ!'
            Logger().logger.info('result:%s', result)
        else:
            result['code'] = '1'
            result['message'] = 'user not find !'
    return result


def modify_password(request):
    Logger().logger.info('now modify  user password  from mobile')
    # insert to db
    result = {'succ': '1'}
    mobile = request.form.get("mobile")
    password = request.form.get("password")
    sms_code = request.form.get("sms_code")
    if password is None or mobile is None  or sms_code is None:
        result['code'] = '1'
        result['message'] = 'password or mobile is null'
        Logger().logger.error('result:%s', result)
        return result
    if session['sms_code'] and session['sms_code']['phone'] == mobile:
        create_time = session['sms_code']['create_time']
        now_time = time.time()
        if now_time-create_time <= constant.const.SEND_SMS_CODE_TIME:
            if sms_code == session['sms_code']['code']:
                user = db_model_user.select_by_mobile(mobile)
                if user:
                    user.password = password
                    db_model_user.update_user(user)
                    session['userinfo'] = {'mobile': mobile, 'name': user.name, 'id': user.id}
                    result['succ'] = 0
                    result['code'] = 0
                    result['message'] = 'modify password succ!'
                else:
                    result['succ'] = 1
                    result['code'] = 1
                    result['message'] = 'user not exist!'
            else:
                result['succ'] = 1
                result['code'] = 3
                result['message'] = 'sms_code error!'
        else:
            result['succ'] = 1
            result['code'] = 2
            result['message'] = 'sms_code overdue!'
    else:
        result['code'] = 4
        result['message'] = 'sms_code is not exist'
    Logger().logger.error('result:%s', result)

    return result


def check_user_name(request):
    name = request.form.get("name")
    Logger().logger.info('check user name:%s', name)
    result = {'succ': 1}
    if name is None or name == '':
        result['succ'] = '0'
        result['code'] = '0'
        result['message'] = 'check user name pass!'
    else:
        user = db_model_user.select_full_match_by_name(name)
        Logger().logger.info('query name result:%s,%s', (name, user))
        if user:
            result['succ'] = '1'
            result['code'] = '1'
            result['message'] = 'user have exist!'
        else:
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'check user name pass!'
    Logger().logger.info('result:%s', result)
    return result


def query_user_info(user_id):
    Logger().logger.info('now query  user info,id：%s',user_id)
    user_info = db_model_user.select_by_id(user_id)
    return user_info


def query_login_user_info():
    user_info = None
    if session.get('userinfo'):
        user_id = session.get('userinfo')['id']
        user_info = db_model_user.select_by_id(user_id)
        return user_info
    else:
        return user_info

def get_user_post(request):
    user_id = request.args.get("user_id")
    view_user_info = db_model_user.select_by_id(user_id)
    page_no = int(request.args.get("no", default_page_no))
    num_perpage = int(request.args.get("size", default_num_perpage))
    paginate = db_model_post.select_all_by_user(page_no, num_perpage, user_id)
    post_list = []
    for post in paginate.items:
        post.create_time = time_format.timestampFormat(post.create_time)
        post_list.append(db_model_post.to_json(post))
    return post_list, page_no, num_perpage, paginate.total, view_user_info, paginate.has_next


def add_relation(request):
    Logger().logger.info('now create user relation')
    # insert db
    user_id = session.get('userinfo')['id']
    login_user = db_model_user.select_by_id(user_id)
    relation_user_id = request.form.get("relation_user_id")
    relation_user = db_model_user.select_by_id(relation_user_id)

    Logger().logger.info('login_user_id:%s,relation_user_id:%s',user_id,relation_user_id)
    data = db_model_user_relation.select_by_user_id(user_id, relation_user_id)  # 是否有关注信息
    relation_data = db_model_user_relation.select_by_user_id(relation_user_id, user_id)  # 对方是否关注自己
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    # update by lxx,2017-04-19 start
    if data is None:
        each_attention = False
        if relation_data and relation_data.is_relation:  # 对方已关注自己
            each_attention = True  # 互相关注
            relation_data.each_attention = each_attention
            relation_data.update_time = update_time
            db_model_user_relation.update(relation_data)
        create_time = update_time
        Logger().logger.info('user_id:%s,relation_user_id:%s', user_id,relation_user_id)
        db_model_user_relation.insert(user_id, relation_user_id, has_relation, create_time, update_time, each_attention)
        # write message
        db_model_message.insert_follow(user_id, relation_user_id)
    elif data and relation_data:  # 已有关注信息
        data.is_relation = True
        if relation_data.is_relation:  # 且对方已关注自己，直接更新 关注、互相关注
            data.each_attention = True
            relation_data.each_attention = True
            relation_data.update_time = update_time
            db_model_user_relation.update(relation_data)
        data.update_time = update_time
        db_model_user_relation.update(data)
    else:
        data.is_relation = True
        data.update_time = update_time
        db_model_user_relation.update(data)
    # end
    Logger().logger.info('record action of follow user')
    action_content = {'user_id': user_id, 'to_user_id': relation_user_id}
    db_model_action.insert(user_id=user_id, action_type_id=db_model_action_type.get_type_id('follow'),
                           action_detail_info=json.dumps(action_content, ensure_ascii=False),
                           create_time=update_time)

    login_user.attention_num += 1
    Logger().logger.info('now update user attention_num:%s', login_user.attention_num)
    db_model_user.update_user(login_user)
    relation_user.by_attention_num += 1
    Logger().logger.info('now update user by_attention_num:%s', relation_user.by_attention_num)
    db_model_user.update_user(relation_user)


def update_relation(request):  # cancel
    Logger().logger.info('now update user relation')
    # update  is_relation = 1
    user_id = session.get('userinfo')['id']
    login_user = db_model_user.select_by_id(user_id)
    relation_user_id = request.form.get("relation_user_id", 0)
    user = db_model_user.select_by_id(relation_user_id)
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    update_time = time.strftime(ISOTIMEFORMAT, time.localtime())

    # cancel attention ,update by lxx,2017-04-19 start
    user_relation = db_model_user_relation.select_by_user_id(user_id, relation_user_id)
    if user_relation.is_relation:
        user_relation.is_relation = False
        user_relation.update_time = update_time
        if user_relation.each_attention:
            user_relation.each_attention = False
            relation_user = db_model_user_relation.select_by_user_id(relation_user_id, user_id)
            relation_user.each_attention = False
            relation_user.update_time = update_time
            db_model_user_relation.update(relation_user)
        db_model_user_relation.update(user_relation)
    # end
    Logger().logger.info('record action of cancel follow user')
    action_content = {'user_id': user_id, 'to_user_id': relation_user_id}
    db_model_action.insert(user_id=user_id, action_type_id=db_model_action_type.get_type_id('cancel_follow'),
                           action_detail_info=json.dumps(action_content, ensure_ascii=False), create_time=update_time)

    login_user.attention_num -= 1
    db_model_user.update_user(login_user)
    Logger().logger.info('now update user attention_num:%s', login_user.attention_num)

    user.by_attention_num -= 1
    Logger().logger.info('now update user by_attention_num:%s', user.by_attention_num)
    db_model_user.update_user(user)


def select_relation_user_id(request):
    Logger().logger.info('now select user relation')
    # select db
    user_id = session.get('userinfo')['id']
    relation_user_id = request.form.get("relation_user_id", 0)
    Logger().logger.info('user_id:%s,relation_user_id:%s', int(user_id), relation_user_id)
    user_relation = db_model_user_relation.select_by_user_id(user_id, relation_user_id)
    if user_relation:
        return user_relation.is_relation
    else:
        return default_relation


def get_unread_message_from_session():
    messages_unread_len = 0
    if session.get('userinfo'):
        Logger().logger.info('get unread message ,session is :%s', session)
        user_id = int(session.get('userinfo')['id'])
        user_info = db_model_user.select_by_id(user_id)
        if user_info:
            messages = user_info.to_user_messages.filter_by(has_read=False).all()
            messages.extend(user_info.private_mess_to_user.filter_by(has_read=False).all())
            messages_unread_len = len(messages)
        Logger().logger.info('unread message length: %s',messages_unread_len)

    return messages_unread_len


def check_login():
    login_flag = False
    if session.get('userinfo'):
        login_flag = True
    return login_flag


def good_friends(request):
    user_id = request.form.get("user_id")
    login_user_id = 0
    Logger().logger.info('into good friends user_id:%s', user_id)
    if session.get('userinfo'):
        login_user_id = int(session.get('userinfo')['id'])
    page_no = int(request.form.get("no", default_page_no))
    num_perpage = int(request.form.get("size", default_num_perpage))
    each_attention = True
    paginate = db_model_user_relation.select_good_friends(user_id, each_attention, page_no, num_perpage)
    Logger().logger.info('total friends:%s', paginate.total)
    json_user = []

    if login_user_id == 0:
        for user_relation in paginate.items:
            user_relation.is_relation = False
            json_user.append(db_model_user_relation.to_json(user_relation))
    else:
        for user_relation in paginate.items:
            # 当前登录的人是否关注个人主页好友
            login_user_relation = db_model_user_relation.select_by_relation(login_user_id, user_relation.user_id,
                                                                            has_relation)
            if not login_user_relation:
                user_relation.is_relation = False
            else:
                user_relation.is_relation = True
            json_user.append(db_model_user_relation.to_json(user_relation))

    return json_user, page_no, num_perpage, paginate.total, paginate.has_next


#  用户创建的社区
def community_create(request):
    user_id = request.form.get("user_id")
    print user_id
    view_user_info = db_model_user.select_by_id(user_id)
    Logger().logger.info('into community owned user_id:%s', user_id)
    page_no = int(request.form.get("no", default_page_no))
    num_perpage = int(request.form.get("size", default_num_perpage))
    paginate = db_model_community.select_by_owner_id_paging(user_id, page_no, num_perpage)
    Logger().logger.info('total community:%s', paginate.total)
    community_list = []
    for item in paginate.items:
        community_list.append(db_model_community.to_json(item))
    return community_list, page_no, num_perpage, paginate.total, view_user_info, paginate.has_next


def update_user(request):
    result = {}
    if session.get('userinfo')['id']:
        try:
            userid = int(session.get('userinfo')['id'])
            user = db_model_user.select_by_id(userid)
            username = request.form.get('user_name')
            user.name = username
            label = request.form.get('user_label')
            user.label = label
            shop_url = request.form.get("shop_url")
            if shop_url is not None:
                user.shop_url = shop_url
            Logger().logger.info('after modify:%s,%s',user.name, user.label)
            db_model_user.update_user(user)
            session['userinfo'] = {'name': user.name, 'id': user.id}
            result['succ'] = '0'
            result['code'] = '0'
            result['message'] = 'update user info succ!'
            session.get('userinfo')['name'] = username
            Logger().logger.info('result:%s',result)
        except Exception, e:
            result['code'] = 1
            result['message'] = 'exception'
            Logger().logger.error('Exception:%s', e)

    else:
        result['code'] = 1
        request['message'] = 'user not login'
        Logger().logger.info('result:%s', result)
    return result


# add by lxx ,2017-07-17
def query_by_name_paging(request):
    name = request.args.get("name")
    num_perpage =3
    paginate = db_model_user.select_by_name_paging(name,default_page_no,num_perpage)
    user_list = []
    for user in paginate.items:
        user_list.append(db_model_user.to_json(user))
    return user_list
