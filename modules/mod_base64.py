#encoding:utf-8
from bs4 import BeautifulSoup
import base64
import os
import time
import random
from Logger import *
from  fdfs_client import client
import constant
default_path = 'http://social.jinrongdao.creditease.cn/images/'
fastfds_default_path = 'http://social.jinrongdao.creditease.cn/'
# default_path = 'http://localhost:6100/images/'
# fastfds_default_path = 'http://jinrongdao.com/'
# base64 code convert to img src
# add by lxx 2017-04-10


def base64_hander(content, path_type):
    soup = BeautifulSoup(content,"html.parser")
    trs = soup.findAll("img")
    length = len(trs)
    Logger().logger.info('cur_path %s', os.getcwd())
    for i in range(length):
        src = trs[i].attrs["src"].encode('utf-8')
        trs[i].attrs["src"] = base64_to_imgurl(src,path_type)
    soup = str(soup).replace('</img>', '')
    return soup


def base64_to_imgurl(src, path_type):
    cur_path = os.getcwd()
    if src.startswith('data:image'):
        save_path = default_path + path_type + '/'
        upload_path = cur_path + '/static/images/' + path_type + '/'
        header = "data:image"
        cur_time = int(time.time())
        image_arr = src.split(",")
        end_index = image_arr[0].index(';')
        start_index = image_arr[0].index('/')
        file_type = src[start_index + 1:end_index]
        Logger().logger.info('file_type %s', file_type)
        rand1 = random.randint(0, 900) + 100
        rand2 = random.randint(0, 90) + 10
        file_name = '%s%s%s%s%s' % (cur_time, rand1, rand2, '.', file_type)
        save_path += file_name
        Logger().logger.info('upload_path %s,file_name %s', upload_path, file_name)
        if header in image_arr[0]:
            image = image_arr[1]
            try:
                decoded_bytes = base64.decodestring(image)
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                upload_path += file_name
                out = open(upload_path, 'w')
                out.write(decoded_bytes)
                out.close()
                # 调用fastdfs
                Logger().logger.info('uploading fastdfs start!')
                fastfds_image_path = fastfds_default_path
                fastdfs_client = client.Fdfs_client(cur_path + constant.const.FAST_DFS_CONF_PATH)
                res = fastdfs_client.upload_by_filename(upload_path)
                Logger().logger.info('fastdfs_upload_result :%s', res)
                if res:
                    save_path = fastfds_image_path + res['Remote file_id']
                    # end
                else:
                    Logger().logger.info('uploading fastdfs fail!')
            except Exception, e:
                Logger().logger.error('exception %s', e)
            return save_path
    else:
        return src

