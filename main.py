# -*- coding: utf-8 -*-
import time
import json

from flask import Flask, request, render_template
from flask import jsonify
from flask import redirect, url_for, session
from functools import wraps

from modules import mod_comment
from modules import mod_community
from modules import mod_image
from modules import mod_login
from modules import mod_logout
from modules import mod_message
from modules import mod_post
from modules import mod_private_message
from modules import mod_reply
from modules import mod_user
from modules import mod_user_community
from modules import mod_verify
from modules.Logger import *
from modules import mod_adverse
from modules import mod_send_sms_code
from modules import mod_identity_auth
from modules import mod_check_IsPhone

'''  BASICAL FUNCTIONS BEGIN  '''

app = Flask(__name__, static_url_path='')
# app.secret_key = "super secret key"
# app.config['SECRET_KEY'] = 'super secret key'
app.config.from_object('config')

default_user_data = []
default_community_data = []


# 定义一个装饰器用于拦截用户登录
def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        # 现在是模拟登录，获取用户名，项目开发中获取session
        username = session.get('userinfo')
        # 判断用户名存在且用户名是什么的时候直接那个视图函数
        if session.get('userinfo'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return decorator


@app.route('/')
# @interceptor(login_required=True)
def default():
    isPhone = mod_check_IsPhone.check_mobile(request)
    if isPhone:
        print 'index_mobile'
        return redirect('/index_mobile')
    return redirect('/index')


@app.route('/error', methods=['GET', 'POST'])
# @interceptor(login_required=False)
def error():
    msg = request.args.get('msg')
    return render_template('error.html', msg=msg)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', msg=e)


'''  BUSSINESS FUNCTIONS BEGIN  '''


@app.route('/search', methods=['GET'])
# @interceptor(login_required=True)
def search():
    comm_list = mod_community.find_match_community(request)
    user_list = mod_user.query_by_name_paging(request)
    post_list = mod_post.find_match_post(request)
    return jsonify(comm_list=comm_list, user_list=user_list, post_list=post_list)


@app.route('/search_result', methods=['GET'])
# @interceptor(login_required=True)
def search_result():
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    comm_list = mod_community.find_match_community(request)
    user_list = mod_user.query_by_name_paging(request)
    post_list = mod_post.find_match_post(request)
    response = mod_adverse.find_adverse(request)
    title = request.args.get("name")
    adverse_list = None
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            adverse_list = data['data']
    else:
        Logger().logger.error("http request fail !")
    template = 'search_result.html'
    isPhone = mod_check_IsPhone.check_mobile(request)
    if isPhone:
        template = 'search_result_mobile.html'
    return render_template(template, mess_dict=mess_dict, messages_unread_num=messages_unread_num,
                           search=title,
                           comm_list=comm_list, user_list=user_list, post_list=post_list, adverse_list=adverse_list)


@app.route('/pay_adverse', methods=['GET'])
def pay_adverse():
    result = mod_adverse.pay_adverse(request)
    return jsonify(code=result['code'], message=result['message'])


@app.route('/community_create', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community_create():
    result = mod_community.service(request)
    return jsonify(code=result['code'], community=result['data'])


@app.route('/community', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def community():
    community, has_join, create_user = mod_community.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    template = 'community.html'
    if community:
        isPhone = mod_check_IsPhone.check_mobile(request)
        print 'mobile'
        if isPhone:
            template = 'community_mobile.html'
        return render_template(template, has_join=has_join, community=community, create_user=create_user,
                               mess_dict=mess_dict, messages_unread_num=messages_unread_num)
    else:
        msg = '页面找不到了'
        Logger().logger.error(msg)
    return redirect(url_for('error', msg=msg))


@app.route('/get_community_post', methods=['GET'])
def get_community_post():
    model, page_no, num_perpage = mod_post.service(request)
    total = model.total
    Logger().logger.info('result total:%s', total)
    return jsonify(post_list=model.items, page_no=page_no, total=total)


@app.route('/get_commend_community', methods=['GET'])
def get_commend_community():
    page_no, num_page, commend_list = mod_community.select_hot_commend_community(request)
    Logger().logger.info('total:%s', len(commend_list))
    return jsonify(page_no=page_no, num_page=num_page, commend_list=commend_list)


@app.route('/update_community', methods=['POST'])
def update_community():
    result = mod_community.service(request)
    Logger().logger.info('result:%s', result)
    return jsonify(result=result['code'])


@app.route('/post_like', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def post_like():
    result = mod_post.service(request)
    return jsonify(code=result['code'], message=result['message'], like_num=result['data'])


@app.route('/post_publish', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def post_publish():
    community = mod_post.service(request)
    return redirect(url_for('community', id=community.id, type='query'))


@app.route('/post', methods=['GET'])
# @interceptor(login_required=True)
def post():
    post = mod_post.service(request)
    if post:
        has_join = mod_user_community.user_has_join_community(post.community_id)
        mess_dict = mod_message.select_unread_num_by_type()
        messages_unread_num = mod_user.get_unread_message_from_session()
        template='post.html'
        isPhone = mod_check_IsPhone.check_mobile(request)
        if isPhone:
            template ='post_mobile.html'
        return render_template(template, post=post, has_join=has_join, messages_unread_num=messages_unread_num,
                               mess_dict=mess_dict)
    else:
        msg = '页面找不到了'
        Logger().logger.error(msg)
        return redirect(url_for('error', msg=msg))


# show reply and best in post.html
@app.route('/get_reply', methods=['GET'])
def get_reply():
    reply_list, best_reply, like_user_dict, page_no, num_perpage, total_page, total = mod_reply.service(request)
    return jsonify(reply_list=reply_list, best_reply=best_reply, like_user_dict=like_user_dict,
                   total_page=total_page, page_no=page_no, num_perpage=num_perpage, total=total)


@app.route('/delete_post', methods=['POST'])
# @interceptor(login_required=True)
def delete_post():
    result = mod_post.delete_post(request)
    Logger().logger.info('result:%s', result)
    return jsonify(result=result['code'])


@app.route('/find_match_post', methods=['GET'])
# @interceptor(login_required=True)
def find_match_post():
    post_list = mod_post.find_match_post(request)
    return jsonify(post_list=post_list)


@app.route('/reply_publish', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def reply_publish():
    reply, replycount, total_page = mod_reply.service(request)
    return jsonify(reply=reply, replycount=replycount, total_page=total_page)


@app.route('/update_reply', methods=['POST'])
# @interceptor(login_required=True)
def reply_update():
    result = mod_reply.update_reply(request)
    return jsonify(result=result['code'])


@app.route('/delete_reply', methods=['POST'])
# @interceptor(login_required=True)
def delete_reply():
    result = mod_reply.service(request)
    return jsonify(code=result['code'], replycount=result['replycount'])


@app.route('/reply_like_status_change', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def reply_like():
    result = mod_reply.reply_like_changed(request)
    return jsonify(code=result['code'], like_num=result['like_num'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if method is get, then show login page only.if post, then deal login request
    if request.method == 'GET':
        isPhone = mod_check_IsPhone.check_mobile(request)
        if isPhone:
            return render_template('login_mobile.html')
        return render_template('login.html')
    elif request.method == 'POST':
        model, next_url = mod_login.service(request)
        return jsonify(code=model['code'], next_url=next_url)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    result = mod_logout.service()
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


@app.route('/user_create_step_2', methods=['GET', 'POST'])
def user_create_step_2():
    return render_template('user_create_step_2.html')


@app.route('/do_user_create', methods=['GET', 'POST'])
def do_user_create():
    model = mod_user.service(request)
    return jsonify(result='succ')


@app.route('/update_user', methods=['POST'])
def update_user():
    result = mod_user.update_user(request)
    return jsonify(result=result['code'])


@app.route('/user_community', methods=['GET', 'POST'])
def user_community():
    community_user_num = mod_user_community.service(request)
    return jsonify(user_num=community_user_num)


@app.route('/read_message', methods=['GET', 'POST'])
def read_message():
    unread_message_num = mod_message.service(request)
    return jsonify(unread_message_num=unread_message_num)


@app.route('/user_info_post', methods=['GET'])
def user_info_post():
    messages_unread_num = mod_user.get_unread_message_from_session()
    mess_dict = mod_message.select_unread_num_by_type()
    view_user_info = mod_user.service(request)
    user_info_type = 'post'
    template = 'user_info_post.html'
    if view_user_info:
        isPhone = mod_check_IsPhone.check_mobile(request)
        if isPhone:
            template = 'user_info_post_mobile.html'
        return render_template(template, mess_dict=mess_dict, messages_unread=messages_unread_num,
                               view_user_info=view_user_info, user_info_type=user_info_type,
                               messages_unread_num=messages_unread_num)
    else:
        msg = '页面找不到了'
        Logger().logger.error(msg)
        return redirect(url_for('error', msg=msg))


# 个人主页-查询用户的帖子
@app.route('/get_user_post', methods=['GET', 'POST'])
def get_user_post():
    Logger().logger.info('do query user post!')
    post_list, page_no, num_perpage, total, view_user_info, has_next = mod_user.get_user_post(request)
    user_info_type = 'post'
    Logger().logger.info('user_info_type:%s', user_info_type)
    return jsonify(post_list=post_list, no=page_no, size=num_perpage, total_size=total, user_info_type=user_info_type,
                   has_next=has_next)


@app.route('/user_info_community_create', methods=['GET'])
def user_info_community_create():
    Logger().logger.info('user_info_community_owned start')
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    view_user_info = mod_user.service(request)
    user_info_type = 'community_create'
    template = 'user_info_community_create.html'
    if view_user_info:
        isPhone = mod_check_IsPhone.check_mobile(request)
        if isPhone:
            template = 'user_info_community_create_mobile.html'
        return render_template(template, mess_dict=mess_dict,
                               messages_unread_num=messages_unread_num, view_user_info=view_user_info,
                               user_info_type=user_info_type)
    else:
        msg = '页面找不到了'
        Logger().logger.error(msg)
        return redirect(url_for('error', msg=msg))


@app.route('/get_user_create_community', methods=['POST'])
def get_user_create_community():
    community_list, page_no, num_perpage, total, view_user_info, has_next = mod_user.community_create(request)
    return jsonify(community_list=community_list, no=page_no, size=num_perpage, total_size=total, has_next=has_next)


# into the followed html
@app.route('/user_info_community_join', methods=['GET'])
def user_info_community_join():
    view_user_info = mod_user.service(request)
    user_info_type = 'community_join'
    messages_unread_num = mod_user.get_unread_message_from_session()
    mess_dict = mod_message.select_unread_num_by_type()
    template = 'user_community_followed.html'
    if view_user_info:
        isPhone = mod_check_IsPhone.check_mobile(request)
        if isPhone:
            template = 'user_community_followed_mobile.html'
        return render_template(template, view_user_info=view_user_info,
                               user_info_type=user_info_type,
                               mess_dict=mess_dict, messages_unread_num=messages_unread_num)
    else:
        msg = '页面找不到了'
        Logger().logger.error(msg)
        return redirect(url_for('error', msg=msg))


# load data:community the user join
@app.route('/community_joined', methods=['GET'])
def community_joined():
    community_list, page_no, num_perpage, total_count, total_pages, has_next = mod_user_community.service(request)
    return jsonify(community_list=community_list, no=page_no, size=num_perpage, totalCount=total_count,
                   totalPages=total_pages, has_next=has_next)


@app.route('/user_info_friend', methods=['GET', 'POST'])
def user_info_friend():
    Logger().logger.info('user_info_friend start')
    view_user_info = mod_user.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    user_info_type = 'friend'
    template = 'user_info_friend.html'
    if view_user_info:
        isPhone = mod_check_IsPhone.check_mobile(request)
        if isPhone:
            template = 'user_info_friend_mobile.html'
        return render_template(template, mess_dict=mess_dict, messages_unread_num=messages_unread_num,
                               view_user_info=view_user_info, user_info_type=user_info_type)
    else:
        msg = '页面找不到了'
        Logger().logger.error(msg)
        return redirect(url_for('error', msg=msg))


@app.route('/get_user_friend', methods=['POST'])
def get_user_friend():
    Logger().logger.info('now do get user friend data!')
    friend_list, page_no, num_perpage, total, has_next = mod_user.good_friends(request)
    return jsonify(friend_list=friend_list, no=page_no, size=num_perpage, total_size=total, has_next=has_next)


@app.route('/community_owned', methods=['GET', 'post'])
# @interceptor(login_required=True)
def get_community_owned():
    communities, page_no, num_perpage, communities_total = mod_user.community_owned(request)
    return jsonify(communities=communities, no=page_no, size=num_perpage, totalsize=communities_total)


@app.route('/good_friends', methods=['GET', 'post'])
# @interceptor(login_required=True)
def get_good_friends():
    friends, page_no, num_perpage, friends_total = mod_user.good_friends(request)
    return jsonify(friends=friends, no=page_no, size=num_perpage, totalsize=friends_total)


# user_info end

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        template = 'register.html'
        isPhone = mod_check_IsPhone.check_mobile(request)
        if isPhone:
            template = 'register_mobile.html'
        return render_template(template)
    Logger().logger.info('now begin verify')
    result = mod_verify.service(request)
    Logger().logger.info('check sms_code result:%s', result)
    if result['code'] == 0:
        Logger().logger.info('verify pass! now begin insert db')
        result, user_info = mod_user.service(request)
    Logger().logger.info('now begin return regist result')
    return jsonify(code=result['code'], message=result['message'])


# 找回密码
@app.route('/modify_user', methods=['GET', 'POST'])
def modify_user():
    result = mod_user.service(request)
    Logger().logger.info('modify user result:%s', result)
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


# 发送短信验证码
@app.route('/send_sms_code', methods=['GET', 'POST'])
def send_sms_code():
    Logger().logger.info('do send sms code !')
    result = mod_send_sms_code.send_sms_code(request)
    return jsonify(code=result['code'], sms_code=result['sms_code'], message=result['message'])


@app.route('/check_mobile_exist', methods=['GET', 'POST'])
def check_mobile_exist():
    result = mod_verify.service(request)
    Logger().logger.info('mobile check result:%s', result)
    return jsonify(code=result['code'], message=result['message'])


@app.route('/check_user_name', methods=['GET', 'POST'])
def check_user_name():
    result = mod_user.service(request)
    return jsonify(succ=result['succ'], code=result['code'], message=result['message'])


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    template = 'find_password.html'
    isPhone = mod_check_IsPhone.check_mobile(request)
    if isPhone:
        template = 'find_password_mobile.html'
    return render_template(template)


@app.route('/index_mobile', methods=['GET'])
def index_mobile():
    # count = mod_post.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    return render_template('index_mobile.html', mess_dict=mess_dict, messages_unread_num=messages_unread_num)


@app.route('/index', methods=['GET'])
def index():
    # count = mod_post.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    isPhone = mod_check_IsPhone.check_mobile(request)
    redirect='index.html'
    if isPhone:
        print 'index_mobile'
        redirect = 'index_mobile.html'
    return render_template(redirect, mess_dict=mess_dict, messages_unread_num=messages_unread_num)


@app.route('/get_hot_post', methods=['GET'])
def good_post_list():
    page_no, num_perpage, post_list, total, has_next = mod_post.service(request)
    return jsonify(page_no=page_no, num_perpage=num_perpage, post_list=post_list, total=total, has_next=has_next)


@app.route('/get_hot_community', methods=['GET'])
def get_hot_community():
    page_no, num_perpage, commend_list = mod_community.service(request)
    return jsonify(page_no=page_no, num_perpage=num_perpage, commend_list=commend_list)


@app.route('/add_relation', methods=['POST'])
# @interceptor(login_required=True)
def add_relation():
    mod_user.add_relation(request)
    return jsonify(result='succ')


@app.route('/cancel_relation', methods=['POST'])
# @interceptor(login_required=True)
def cancel_relation():
    mod_user.update_relation(request)
    return jsonify(result='succ')


@app.route('/select_relation', methods=['POST'])
# @interceptor(login_required=True)
def select_relation():
    is_relation = mod_user.select_relation_user_id(request)
    return jsonify(is_relation=is_relation)


@app.route('/upload_head_image', methods=['POST'])
# @interceptor(login_required=True)
def upload_head_image():
    Logger().logger.info('upload_head_image')
    result = mod_image.service(request)
    if result.get('code') == 0:
        return jsonify(code=0, result='succ', data=result['data'])
    else:
        return jsonify(code=1, result='fail', data='')


@app.route('/get_default_image', methods=['get'])
# @interceptor(login_required=True)
def get_default_image():
    type = request.args.get("type")
    if type == "user":
        return jsonify(result=default_user_data)
    else:
        return jsonify(result=default_community_data)


# more comment
@app.route('/get_comment', methods=['get'])
# @interceptor(login_required=True)
def get_comment():
    Logger().logger.info('get_comment')
    paginate = mod_comment.service(request)
    return jsonify(comment_list=paginate.items, has_next=paginate.has_next)


@app.route('/publish_comment', methods=['post'])
# @interceptor(login_required=True)
def publish_comment():
    result = mod_comment.service(request)
    Logger().logger.info('result:%s', result)
    return jsonify(code=result['code'], comment=result['comment'])


@app.route('/delete_comment', methods=['post'])
# @interceptor(login_required=True)
def delete_comment():
    Logger().logger.info('delete_comment')
    result = mod_comment.service(request)
    Logger().logger.info('result:%s', result)
    return jsonify(result=result['code'])


@app.route('/message', methods=['GET', 'POST'])
# @interceptor(login_required=True)
def get_message():
    Logger().logger.info('get_message')
    login_flag = mod_user.check_login()
    if not login_flag:
        Logger().logger.error('user not login')
        return redirect('/index')
    messages_unread_num = mod_user.get_unread_message_from_session()
    read_list, unread_list, total, page_no, num_perpage, message_type = mod_message.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    view_user_info = mod_user.service(request)
    isPhone = mod_check_IsPhone.check_mobile(request)
    template = 'message.html'
    if isPhone:
        template = 'message_mobile.html'
    return render_template(template, messages_unread_num=messages_unread_num, view_user_info=view_user_info,
                           mess_dict=mess_dict, message_type=message_type, read_list=read_list, unread_list=unread_list,
                           unread_num=len(unread_list), read_num=len(read_list), total_size=total, size=num_perpage,
                           no=page_no)


@app.route('/private_message', methods=['GET', 'POST'])
# @interceptor(login_required=True)
@login_required
def private_message():
    to_user, user_list, unread_count_list, user_num = mod_private_message.select_recent_user(request)
    ISOTIMEFORMAT = '%Y-%m-%d'
    today = time.strftime(ISOTIMEFORMAT, time.localtime())
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    template = 'private_message.html'
    isPhone = mod_check_IsPhone.check_mobile(request)
    if isPhone:
        template = 'private_message_mobile.html'
    return render_template(template, today=today, to_user=to_user, user_list=user_list,
                           unread_count_list=unread_count_list, user_num=user_num, mess_dict=mess_dict,
                           messages_unread_num=messages_unread_num)


@app.route('/save_message', methods=['GET', 'POST'])
# @interceptor(login_required=True)
@login_required
def save_essage():
    data = mod_private_message.save_private_message(request)
    return jsonify(result=data)


@app.route('/get_new_message', methods=['GET', 'POST'])
# @interceptor(login_required=True)
@login_required
def new_essage():
    data = mod_private_message.service(request)
    return jsonify(result=data)


# to do  点击人后加载此用户聊天信息
@app.route('/get_history_message', methods=['GET'])
# @interceptor(login_required=True)
@login_required
def get_history_message():
    mess_list, has_next = mod_private_message.service(request)
    return jsonify(result=mess_list, has_next=has_next)


@app.route('/user_auth', methods=['GET'])
@login_required
def user_auth():
    Logger().logger.info('user_info_friend start')
    view_user_info = mod_user.service(request)
    mess_dict = mod_message.select_unread_num_by_type()
    messages_unread_num = mod_user.get_unread_message_from_session()
    user_info_type = 'auth'
    data_person_status, data_finance_status = mod_identity_auth.query_user_auth()
    template = 'user_authentication.html'
    isPhone = mod_check_IsPhone.check_mobile(request)
    if isPhone:
        template = 'user_authentication_mobile.html'
    return render_template(template, mess_dict=mess_dict, messages_unread_num=messages_unread_num,
                           view_user_info=view_user_info, user_info_type=user_info_type,
                           auth_person_status=data_person_status,
                           auth_finance_status=data_finance_status)


@app.route('/do_user_auth', methods=['POST'])
def do_user_auth():
    Logger().logger.info('do_user_auth start')
    result = mod_identity_auth.service(request)
    return jsonify(code=result['code'], message=result['message'])


'''  MAIN ENTRY  '''
if __name__ == '__main__':
    app.debug = True
    ##项目启动 只查询一次默认图片数据
    user_data, comm_data = mod_image.select_default_image()
    default_user_data = user_data
    default_community_data = comm_data
    app.run(host="0.0.0.0", port=6100, processes=6)
