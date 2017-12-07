#!/usr/bin/env python
# encoding: utf-8

import os
import datetime

from Celery import crontab

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # generate 32 SECRET_KEY from random choices('a-z0-9') command:
    # Bash:
    # cat /dev/urandom | tr -cd 'a-z0-9' | head -c 32
    # Mac:
    # cat /dev/urandom | env LC-CTYPE=C tr -cd 'a-z0-9' | head -c 32
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hard to guess string')
    RECAPTCHA_PUBLIC_KEY=""
    RECAPTCHA_PRIVATE_KEY=""
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

    # 针对 NoSQL 的数据库操作，选用 MongoDB
    # MongoDB 连接配置
    MONGODB_SETTINGS = {
        'db': 'local',
        'host': 'localhost',
        'port': 27017
    }

    # celery + redis 的配置
    # the URL is in the format of:
    # redis://:password@hostname:port/db_number
    # CELERY_BACKEND_URL = 'redis://localhost:6379/0'
    REDIS_URL = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # 设定一个定期执行的任务
    CELERY_SCHEDULE = {
        # 每间隔30秒执行一次
        'log-every-30-secondes': {
            'task': 'webapp.tasks.log',
            'schedule': datetime.timedelta(seconds=30),
            'args': ("Message",)
        },
        'weekly-digest': {
            'task': 'weebapp.task.digest',
            'schedule': crontab(day_of_week=6, hour='10')
        },
    }


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,

    'default': DevConfig
}
