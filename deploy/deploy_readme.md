1.修改链接数据库的配置:
  modules/db_interface/db_connect.py 中的app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/social'
2.修改连接fastfast的配置
  fdfs_client/client.conf
2.修改程序启动的配置
  main.py 里的app.run(host="0.0.0.0") 
