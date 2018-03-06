# coding=utf-8
import json
import time

import jieba
from flask import session

from db_interface import db_model_action
from db_interface import db_model_action_type
from db_interface import db_model_community
from db_interface import db_model_inverted_index
from db_interface import db_model_post
from db_interface import db_model_reply
from db_interface import db_model_post_like_stat
from db_interface import db_model_user
from db_interface import db_model_user_community
from  db_interface import db_model_comment
from modules import mod_base64
from modules import mod_lcs
from modules import time_format
from Logger import *
default_page_no = 1
default_num_perpage = 10
default_community_id = 0
default_post_id = 0
default_percent = 0.85


def service(request):
    if request.method == 'POST':
        type = request.form.get("type")
        if type == "publish":
            return publish_post(request)
        if type == "like":
            return post_like(request)
        else:
            Logger().logger.error('error request:%s',request)
    elif request.method == 'GET':
        type = request.args.get("type")
        if type =='getpost':
            return query_post_in_community(request)
        elif type=='postInfo':
            return post_info(request)
        elif type == 'hot':  # 首页热帖
            return select_hot_post(request)
        elif type == 'delete':
            return delete_post(request)
        else:
            Logger().logger.error('error request:%s',request)


def find_match_post(request):
    title = request.args.get("name")
    words = list(jieba.cut(title.strip(), cut_all=False))
    post_ids = []
    post_list = []
    dict_post = {}
    for word in words:
        data = db_model_inverted_index.select_by_word(word)
        if data:
            post_ids = list(set(post_ids + str(data.post_id).split(',')))
            post_id_array = str(data.post_id).split(',')
            [post_ids.append(item) for item in post_id_array if item not in post_ids]
    # lcs
    for id in post_ids:
        post = db_model_post.select_by_id(id)
        if post:
            lcs_list, flag = mod_lcs.lcs(title, post.title)
            lcs_title = []
            lcs_title = mod_lcs.printLcs(flag, title, len(title), len(post.title), lcs_title)
            lcs_title = ''.join(lcs_title)
            # 匹配百分比
            percent = len(lcs_title.strip()) / float(len(title.strip()))
            dict_post[id] = percent  # dict:{'post_id':'percent',}
            # print 'id', id, 'lcs_title', lcs_title, 'percent', '%.2f' % percent
    if dict_post:
        # 按percent 由大到小排序
        dict_list = sorted(dict_post.items(), key=lambda e: e[1], reverse=True)
        # 从元组取值
        key = dict_list[0][0]
        value = dict_list[0][1]
        # 保留2位小数
        max_percent = round(value, 2)
        Logger().logger.info('key: %s,value:%s', key, value)
        ids = []
        if max_percent > default_percent:
            for item in dict_list:  # 遍历元素是元组的集合
                if item[1] < default_percent:
                    break
                ids.append(item[0])
            ids = ','.join(ids)
            paginate = db_model_post.select_by_ids(ids, default_page_no, default_num_perpage)
            for item in paginate.items:
                post_list.append(db_model_post.to_json(item))
    return post_list


def delete_post(request):
    post_id = request.form.get("post_id")
    post = db_model_post.select_by_id(post_id)
    result = {}
    if post is None:
        result['code'] = 1
        result['message'] ='delete fail,post is not find'
        return result
    try:
        post.status = 1
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        update_time = time.strftime(ISOTIMEFORMAT, time.localtime())
        post.last_update_time = update_time
        db_model_post.update(post)
        # to do 删除分词的postid
        inverted_index_list = db_model_inverted_index.select_by_post_id(post.id)
        for item in inverted_index_list:
            post_id_list = item.post_id.split(',')
            post_id_list.remove(str(post.id))
            item.post_id = ','.join(post_id_list)
            item.last_update_time = update_time
            db_model_inverted_index.update(item)
        Logger().logger.info('delete inverted_index success!')
        community = db_model_community.select_by_id(post.community_id)
        # update community post_num
        community.post_num -= 1
        db_model_community.update(community)
        Logger().logger.info('update community post_num done!')
        # update user post_num
        user = db_model_user.select_by_id(post.create_user_id)
        user.post_num -= 1
        db_model_user.update_user(user)
        Logger().logger.info('update user post_num done!')
        # dele reply,comment
        for reply in post.replys:
            reply.status =1
            for comment in reply.comments:
                comment.status =1
                db_model_comment.update_comment(comment)
            db_model_reply.update(reply)
        result['code'] = 0
        result['message'] = 'delete success !'
    except Exception, e:
        result['code'] = 1
        result['message'] = 'delete Exception !'
        Logger().logger.error('Exception:%s',e)
    Logger().logger.info('delete post:%s', post_id)

    return result


def publish_post(request):
    Logger().logger.info('now publish post request')
    # insert to db
    title = request.form.get("title")
    content = request.form.get("content")
    path_type = 'post'
    content = mod_base64.base64_hander(content, path_type)
    community_id = request.form.get("community_id", 1)
    community = db_model_community.select_by_id(community_id)
    if not session.get('userinfo'):
        Logger().logger.info('user not login  return !')
        return community
    create_user_id = session.get('userinfo')['id']
    token = session.get('token')
    publish_token = request.form.get("token")
    Logger().logger.info('session token: %s,publish_token: %s', token, publish_token)
    if not token or not publish_token or str(token) != str(publish_token):
        Logger().logger.info('post can not repeat publish  return !')
        return community
    login_user = db_model_user.select_by_id(create_user_id)
    floor_num = 0
    like_num = 0
    status = 0
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    last_update_time = create_time
    Logger().logger.info('title:%s,content:%s,user_id:%s,community_id:%s',title,content,create_user_id,community_id)
    insert = db_model_post.insert(title, content, create_user_id, community_id, floor_num,like_num, create_time,
                                  last_update_time, status)
    Logger().logger.info('now insert to db')
    Logger().logger.info('record action of create post')
    action_content = {'post_id': insert.id}
    db_model_action.insert(user_id=create_user_id,
                           action_type_id=db_model_action_type.get_type_id('create_post'),
                           action_detail_info=json.dumps(action_content, ensure_ascii=False),
                           create_time=create_time)

    login_user.post_num += 1
    Logger().logger.info('now update post_num to db %s',login_user)

    # insert into inverted_index
    last_update_time = create_time
    # fenci
    words = list(jieba.cut(title.strip(), cut_all=False))
    Logger().logger.info('words length %s',len(words))
    for word in words:
        inverted_index = db_model_inverted_index.select_by_word(word)
        if inverted_index :
            post_id_list = str(inverted_index.post_id).split(',')
            if not insert.id in post_id_list:
                post_id_list.append(str(insert.id))
                inverted_index.post_id = ','.join(post_id_list)
                inverted_index.last_update_time = last_update_time
                db_model_inverted_index.update(inverted_index)
        else:
            db_model_inverted_index.insert(word, insert.id, create_time, last_update_time)
    Logger().logger.info('now insert into inverted_index')
    community.post_num += 1
    db_model_community.update(community)
    session['token'] = None
    return community


def query_post_in_community(request):
    community_id = request.args.get("community_id", default_community_id)
    Logger().logger.info('now query post in communit id:%s',community_id)
    page_no = int(request.args.get("page_no", default_page_no))
    num_perpage = int(request.args.get("num_perpage", default_num_perpage))
    # select post indb
    paginate = db_model_post.select_all_paging(page_no, num_perpage, community_id)
    # return select value
    paginate.items = formate_post_time(paginate.items)
    return paginate, page_no, num_perpage


def post_info(request):
    post_id = request.args.get("id", default_post_id)
    Logger().logger.info('now do query post,id:'+post_id)
    # select db
    post = db_model_post.select_by_id(post_id)
    if post:
        post.create_time = time_format.timestampFormat(post.create_time)
        post.like_status = False
        if session.get('userinfo'):
            user_id = session.get('userinfo')['id']
            post.like_status = db_model_post_like_stat.is_post_liked_by_user(post_id, user_id)
    return post


def select_hot_post(request):
    max_number = 1000
    page_no = int(request.args.get("page_no", default_page_no))
    num_perpage = int(request.args.get("num_perpage", default_num_perpage))
    if page_no > (max_number/num_perpage):
        page_no = (max_number/num_perpage)
    # select db
    paginate = db_model_post.select_post_by_floor_num(page_no, num_perpage)
    post_list = formate_post_time(paginate.items)
    if paginate.total>max_number:
        total =max_number
    else:
        total = paginate.total
    return page_no, num_perpage, post_list,total, paginate.has_next


def formate_post_time(post_list):
    post_list_new = []
    for post_new in post_list:
        post_new.create_time = time_format.timestampFormat(post_new.create_time)
        post_list_new.append(db_model_post.to_json(post_new))
    return post_list_new


def post_like(request):
    result = {}
    try:
        if session.get('userinfo'):
            user_id = session.get('userinfo')['id']
            post_id = request.form.get('post_id')
            status = request.form.get('status')
            post = db_model_post.select_by_id(post_id)
            Logger().logger.info('now do update post like num')
            if status == 'true':
                status = True
                post.like_num += 1
            else:
                status = False
                post.like_num -= 1
            Logger().logger.info('now do add post like user_id:%s,post_id:%s', user_id, post_id)
            ISOTIMEFORMAT = '%Y-%m-%d %X'
            create_time = time.strftime(ISOTIMEFORMAT, time.localtime())
            db_model_post_like_stat.insert_or_update(post_id, user_id, create_time, status)
            db_model_post.update(post)
            result['code'] = 0
            result['message'] = 'success'
            result['data'] = post.like_num
        else:
            result['code'] = 1
            result['message'] = 'user not login!'
            result['data'] = ''
    except Exception, e:
        print e
        result['code'] = 1
        result['message'] = 'fail'
        result['data'] = ''
    return result


