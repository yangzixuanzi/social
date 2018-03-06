# -*- coding: utf-8 -*-
import logging
from SafeRotatingFileHandler import *
import os


# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger(logging.Logger):

    def __init__(self):

        format = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
        logName = os.getcwd()+'/logs/social_info.log'
        formatter = logging.Formatter(format)

        self.logger = logging.getLogger("logger")  # name 相同返回同一个logger
        self.logger.setLevel(logging.INFO)
        fileTimeHandler = SafeRotatingFileHandler(logName, "midnight",1,backupCount=10)  # 这个文件跟之前的文件有重名，则会自动覆盖掉以前的文件
        fileTimeHandler.suffix = "%Y-%m-%d" # "%Y-%m-%d"  # 切割后文件 social_info.log.YYYY-mm-dd
        fileTimeHandler.setLevel(logging.INFO)
        fileTimeHandler.setFormatter(formatter)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(fileTimeHandler)  # 输出到文件
            self.logger.addHandler(consoleHandler)  # 输出到控制台

