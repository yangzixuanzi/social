# coding=utf-8
import const
# 在这里定义常量
const.ADVERSE_PAYMENT_URL = 'http://127.0.0.1:8081/adverse/payment'

const.ADVERSE_MATCHED_ADVERSE_URL = "http://127.0.0.1:8081/adverse/matched_adverse"

const.SEND_SMS_CODE = "http://10.130.32.21:8080/alarm/sendmessage"

const.SEND_SMS_CODE_TIME = 300  # 手机验证码5分钟内有效

const.FAST_DFS_CONF_PATH = '/program/fdfs_client/client.conf'  # fast_dfs 配置文件路径

const.CHECK_STATUS_ONCHECK = 1  # 待审核，审核中

const.CHECK_STATUS_CHECK_PASS = 2  #审核通过

const.CHECK_STATUS_CHECK_NO_PASS = 3  #审核未通过

const.AUTH_TYPE_PERSONAL = 1  # 个人认证

const.AUTH_TYPE_FINANCE_CONSULTANT = 2  # 理财师认证
