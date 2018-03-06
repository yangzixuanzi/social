# -*- coding: utf-8 -*-
from fdfs_client.client import *
# 这个是测试fastdfs 上传文件的

'''  MAIN ENTRY  '''
if __name__ == '__main__':
    client = Fdfs_client('client.conf')
    ret = client.upload_by_filename('test.txt')
    print ret