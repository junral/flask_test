#!/usr/bin/env python
# encoding: utf-8

import os


class Config(object):
    pass


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


class DevConfig(object):
    """ 开发环境配置 """
    DEBUG = True
    # SQLite
    # BASE_URL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # DB_URI = 'sqlite:///' + os.path.join(BASE_URL, 'database.db')
    DB_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查看数据库 SQL 查询语句设置
    # SQLALCHEMY_ECHO = True
