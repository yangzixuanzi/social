线上部署步骤：
1.在39\40新建/data/yx/svr/finance_one/social_new/目录,整个工程拷贝到该目录下
2.修改链接数据库的配置:
  modules/db_interface/db_connect.py 中的app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@10.120.66.39/social'
3.修改连接fastfast的配置
  fdfs_client/client.conf tracker server ip 改为10.120.66.39
4.如果未初始化过数据库则初始化: /usr/local/python/bin/python modules/ modules/create_table.py
5.测试 /usr/local/python/bin/python main.py 看运行效果
6.没问题的话mv social_new social 
7.nohup /usr/local/python/bin/python main.py --social > social.log 2>&1 & 启动程序


本地部署：
1.grep jinrongdao.creditease.corp ./ -r,把所有搜索相关的域名加上5100端口，社区相关的加上6100端口
2.修改 /etc/hosts 文件，加上映射：
  127.0.0.1       jinrongdao.creditease.corp
  127.0.0.1       social.jinrongdao.creditease.corp
3.pyhton main.py 启动
4. 在浏览器输入jinrongdao.creditease.corp:6100测试效果
# social
# a bbs system 
