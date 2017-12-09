#!/usr/bin/env python
# coding: utf-8

import time
import unittest
# import threading
from selenium import webdriver


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Firefox
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            # cls.app = create_app('testing')
            # cls.app_context = cls.app.app_context()
            # cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # create the database and populate with some fake data
            # db.create_all()
            # Role.insert_roles()
            # User.generate_fake(10)
            # Post.generate_fake(10)

            # add an administrator user
            # admin_role = Role.query.filter_by(permissions=0xff).first()
            # admin = User(email='john@example.com',
                         # username='john', password='cat',
                         # role=admin_role, confirmed=True)
            # db.session.add(admin)
            # db.session.commit()

            # start the Flask server in a thread
            # threading.Thread(target=cls.app.run).start()

            # give the server a second to ensure it is up
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.close()
            # stop the flask server and the browser
            # cls.client.get('http://localhost:5000/shutdown')
            # cls.client.close()

            # # destroy database
            # db.drop_all()
            # db.session.remove()

            # # remove application context
            # cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    # def setUp(self):
        # self.driver = webdriver.Firefox()

    # def tearDown(self):
        # self.driver.close()

    def test_add_new_post(self):
        """ 测试是否使用文章创建页面新增一篇文章

            1. 用户登录网站
            2. 前往新文章创建页面
            3. 填写表单各域，并提交表单
            4. 前往博客首页，确认这篇新文章出现在首页
        """
        # pass

        # 登录
        self.driver.get('http://localhost:5000/login')

        username_field = self.driver.find_element_by_name(
            "username"
        )
        username_field.send_keys('test')

        password_field = self.driver.find_element_by_name(
            'password'
        )
        password_field.send_keys('test')

        login_button = self.driver.find_element_by_name(
            'Login'
        )
        login_button.click()

        # 填写表单
        self.driver.get('http://localhost:5000/blog/new')

        title_field = self.driver.find_element_by_name('title')
        title_field.send_keys('Test Title')

        # 定位到 iframe 里面的编辑器
        # switch_to 方法可以切换驱动的上下文，从而允许进入另一个
        # iframe 里面去选择元素。
        self.driver.switch_to.fram(
            self.driver.find_element_by_tag_name('iframe')
        )
        post_field = self.driver.find_element_by_class_name(
            'cke_editable'
        )

        post_field.add_keys('Test content')
        self.driver.switch_to.parent_frame()

        post_button = self.driver.find_element_by_name(
            'Submit'
        )
        post_button.click()

        # 确认文章已经创建
        self.driver.get('http://localhost:5000/blog')
        self.assertIn('Test Title', self.driver.page_source)
        self.assertIn('Test content', self.driver.page_source)
