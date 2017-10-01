# 配置文件

import os

DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'zing_qa'
USERNAME = 'root'
PASSWORD = 'password'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
    PASSWORD, HOSTNAME, PORT, DATABASE)
