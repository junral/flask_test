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
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hard to guess string')
    # pass

    @staticmethod
    def init_app(app):
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
    # pass

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to administrator
        import logging
        from logging.handler import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASK_MAIL_SENDER,
            toaddrs=[cls.FLASK_ADMIN],
            subject=cls.FLASK_MAIL_SUBJECT_PREFIX + 'Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setlevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class TestConfig(Config):
    """ 测试环境配置 """
    TESTING = True
    # SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(BASE_DIR, '../database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False


class DevConfig(Config):
    """ 开发环境配置 """
    DEBUG = True
    # SQLite
    # DB_URI = 'sqlite:///database.db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(BASE_DIR, '../database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查看数据库 SQL 查询语句设置
    # SQLALCHEMY_ECHO = True


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,

    'default': DevConfig
}