#!/usr/bin/env python
# encoding: utf-8

# from HTMLParser import HTMLParser
from purifier.purifier import HTMLParser
from flask_restful import fields


# 自定义字段类型
# 用于把字符串中的HTML标签过滤掉
class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    """
    清除任何字符串中的HTML标签，返回纯文本
    """
    s = HTMLStripper()
    s.feed(html)

    return s.get_data()


class HTMLField(fields.Raw):
    def format(self, value):
        return strip_tags(str(value))
