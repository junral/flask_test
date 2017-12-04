#!/usr/bin/env python
# encoding: utf-8

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # generate 32 SECRET_KEY from random choices('a-z0-9') command:
    # Bash:
    # cat /dev/urandom | tr -cd 'a-z0-9' | head -c 32
    # Mac:
    # cat /dev/urandom | env LC-CTYPE=C tr -cd 'a-z0-9' | head -c 32
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # pass


class ProdConfig(object):
    """ 生产环境配置 """
    # MYSQL
    # mysql+pymysql://user:password@ip:port/db_name
    # Postgres
    # postgresql+psycopg2://user:password@ip:port/db_name
    # MSSQL
    # mssql+pyodbc://user:password@dsn_name
    # Oracle
    # oracle+cx_oracle://user:password@ip:port/db_name
    pass


class DevConfig(Config):
    """ 开发环境配置 """
    DEBUG = True
    # SQLite
    DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    # DB_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查看数据库 SQL 查询语句设置
    # SQLALCHEMY_ECHO = True
