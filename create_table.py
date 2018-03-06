# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask import jsonify
from flask import redirect, url_for

# import os
# import sys
#sys.path.append(os.path.abspath('../../'))

# import mod_community
# import mod_login
# import mod_logout
# import mod_post
# import mod_reply
# import mod_user
# import mod_user_community
# import time_format
from modules.db_interface import db_model_user_relation
from modules.db_interface import db_default_image
from modules.db_interface import db_model_message_type
from modules.db_interface import db_model_message
from modules.db_interface import db_model_verify
from modules.db_interface import db_model_comment
from modules.db_interface import db_model_reply
from modules.db_interface import db_model_user
from modules.db_interface import db_model_community
from modules.db_interface import db_model_post
from modules.db_interface import db_model_reply_like_stat
from modules.db_interface import db_model_user_community
from modules.db_interface import db_model_user_relation
from modules.db_interface import db_model_private_message
from modules.db_interface import db_model_action
from modules.db_interface import db_model_action_type
from modules.db_interface import  db_model_inverted_index
from modules.db_interface import db_model_post_like_stat
from modules.db_interface import db_model_identity_authentication


'''  BASICAL FUNCTIONS BEGIN  '''

#app = Flask(__name__, static_url_path='')
# app.secret_key = "super secret key"
# app.config['SECRET_KEY'] = 'super secret key'
#app.config.from_object('config')

# 建表语句，在social下执行
'''  MAIN ENTRY  '''
if __name__ == '__main__':
#    app.debug = True
    # print 'create table start'
    # print 'create table default_image...'
    # db_default_image.create_table()
    # print 'create default user image...'
    # db_default_image.create_default_user_img()
    # print 'create default community image...'
    # db_default_image.create_default_community_img()
    # print 'create table user_relation...'
    # db_model_user_relation.create_table()
    # print 'create table message_type...'
    # db_model_message_type.create_table()
    # print 'insert value to table message_type...'
    # db_model_message_type.insert_default_value()
    # print 'create table message...'
    # db_model_message.create_table()
    # print 'create table verify...'
    # db_model_verify.create_table()
    # db_model_comment.create_table()
    # db_model_reply.create_table()
    # db_model_user.create_table()
    # db_model_community.create_table()
    # db_model_post.create_table()
    # db_model_reply_like_stat.create_table()
    # db_model_user_community.create_table()
    # db_model_user_relation.create_table()
    # db_model_private_message.create_table()
    # print 'create table private message...'
    # print 'create table action...'
    # db_model_action.create_table()
    # print 'create table action type...'
    # db_model_action_type.create_table()
    # print 'insert default action type value...'
    # db_model_action_type.insert_default_value()
    # print 'create table inverted_index'
    # db_model_inverted_index.create_table()
    # print 'create table end'
    # db_model_post_like_stat.create_table()
    #print 'post_like_stat create table end'
    db_model_identity_authentication.create_table()
    print 'identity_authentication create table end'


