#!/usr/bin/env python
# encoding: utf-8

import datetime

# from flask import render_template
# from email.mime.text import MIMEText

from .extensions import celery
from .models import Reminder, Post
from .email import send


@celery.task()
def log(msg):
    return msg


@celery.task()
def multiply(x, y):
    return x * y


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def reminder(self, pk):
    reminder = Reminder.query.get(pk)
    send(
        reminder.email,
        'Your reminder',
        'reminder',
        {'text': reminder.text}
    )
    #  msg = MIMEText(reminder.text)
    #  msg['Subject'] = 'your reminder'
    #  msg['Form'] = 'junral@163.com'
    #  msg['To'] = reminder.email

    #  try:
        #  smtp_server = smtplib.SMTP('localhost')
        #  smtp_server.starttls()
        #  smtp_server.login('junral', 'wujunrong1994;')
        #  smtp_server.sendmail(
            #  'junral@163.com',
            #  [reminder.email],
            #  msg.as_string()
        #  )
        #  smtp_server.close()
        #  return
    #  except Exception as e:
        #  self.retry(exc=e)


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def digest(self):
    # 找出这周的起始和结束日
    year, week = datetime.datetime.now().isocalendar()[0:2]
    date = datetime.date(year, 1, 1)
    if (date.weekday() > 3):
        date = date + datetime.timedelta(days=7 - datetime.weekday())
    else:
        date = date - datetime.timedelta(days=date.weekday())
    delta = datetime.timedelta(days=(week - 1) * 7)
    start, end = date + delta, date + delta + datetime.timedelta(days=6)

    posts = Post.query.filter(
        Post.publish_date >= start,
        Post.publish_date <= end
    ).all()

    if (len(posts) == 0):
        return
    send(
        reminder.emial,
        '',
        'digest',
        {'posts': posts}
    )

    #  msg = MIMEText(
        #  render_template("digest.html", posts=posts),
        #  'html'
    #  )

    #  msg['Subject'] = 'Weekly Digest'
    #  msg['Form'] = ''

    #  try:
    #  smtp_server = smtplib.SMTP('localhost')
    #  smtp_server.starttls()
    #  smtp_server.login('junral', 'wujunrong1994;')
    #  smtp_server.sendmail(
        #  'junral@163.com',
        #  [reminder.email],
        #  msg.as_string()
    #  )
    #  smtp_server.close()
        #  return
    #  except Exception as e:
        #  self.retry(exc=e)



def on_reminder_save(mapper, connect, self):
    reminder.apply_async(args=(self.id), eta=self.date)


# 如果一个任务失败可以通过 retry() 方法再次调用自己，如下所示：
# @celery.task(bind=True)
# def task():
# try:
# some_code
# except Exception as e:
# self.retry(exc=e)

#  bind 参数会通知 Celery 在调用函数时，把任务对象作为第1个参数传入。
#  这样就可以通过 self 参数访问任务对象，并调用 retry 方法，它会使用
#  相同的参数把任务重跑一次。
#  更多参数及其相应的行为：
#  max_retries: 任务可以重试的最大次数。达到该次数后，任务将被标记为失败
#  default_retry_delay: 以秒为单位，表示重跑任务之前应该等待的时间。
#  rate_limit: 限定了在一段给定时间内这个任务最多能进行多少次不同的调用。
#  如果这个值是一个整数，则意味着每秒钟允许这个任务跑多少次，这个值也可以
#  是 x/m 格式的字符串，意味着每分钟跑 x 次，或者 x/h，意思是每小时跑 x 次。
#  time_limit: 如果带了这个参数，且任务运行时间超过了此参数规定的秒数，就会把任务杀掉
#  ignore_result: 如果任务的返回值没有被使用，就不要把值传回

#  celery 工作流：
#  签名（signature）的使用：
#  from celery import signature
#  调用签名时，使用跟 apply_async 同样的参数：
#  >>> signature('webapp.tasks.multiply', args=(4, 4), countdown=10)
#  webtask.multiply(4, 4)
#  >>> from webapp.tasks import multiply
#  >>> multiply.substask((4, 4), countdown=10)
#  webtask.multiply(4, 4)
#  # 上一功能的缩略版本，和 delay 方法一样，没有 apply_async 的关键字参数
#  >>> multiply.s(4, 4)
#  webtask.multiply(4, 4)
#  >>> multiply.s(4, 4)()
#  16
#  在调用一个任务的签名（或者叫子任务）时，就生成了一个函数，可以把它传给其它函数，让
#  其它函数去执行它。如果直接执行这个签名，就会在当前进程中执行，而不是在工作进程中执行
#  >>> multiply.s(4, 4).delay()

#  偏函数：
#  任务签名的第一个应用是具有函数是编程风格的特性：偏函数。偏函数（partial）来源于
#  一个要接收很多参数的函数，这个函数被施加某种操作后，生成了一个新的函数，在调用
#  这个函数时，前n个参数永远是一样的。
#  >>> partial = multiply.s(4)
#  >>> partial.delay(4)
#  16
#  事实上，我们创建了一个作为偏函数保存的新函数，这个函数永远只接收一个参数，并将其乘以4

#  回调函数：
#  适用于当一个任务完成时，需要基于这个任务执行结构去执行另一个任务，为了实现这个目的，apply_async
#  函数提供了一种 link 方法：
#  >>> multiply.apply_async((4, 4), link=log.s())
#  如果回调函数不接收输入，或者不需要上一个任务输出的结果，则其任务签名就必须使用
#  si 方法，并设置为不可变（immutable）类型：
#  >>> multiply.apply_async((4, 4), link=log.si('Message'))

#  偏函数和回调函数可以结合起来使用，以实现某些强大的功能：
#  >>> multiply.apply_async((4, 4), link=multiply.s(4))
#  如果使用 get 方法获取了结果，结果会是16，而不是64，因为 get 方法不会返回回调函数的结果

#  任务组：
#  任务组（group）函数接收一组任务签名的列表，并生成一个函数，调用该函数可并行执行所有的任务签名，
#  并返回所有结果的列表：
#  from celery import group
#  >>> sig = group(multiply.s(i, i + 5) for i in range(10))
#  >>> result = sig.delay()
#  >>> result.get()
#  [0, 6, 14, 24, 36, 50, 66, 84, 104, 126]

#  任务链：
#  任务链（chain）函数接收一组任务签名，把每个签名的执行结果传给任务链中的下一个，最后只会返回
#  一个结果，如下所示：
#  >>> from celery import chain
#  >>> sig = chain(multiply.s(10, 10), multiply.s(4), multiply.s(20))
#  也可写成：
#  >>> sig = (multiply.s(10, 10) | multiply.s(4) | multiply.s(20))
#  >>> result = sig.delay()
#  >>> result.get()
#  8000

#  任务链和偏函数可以做更多的事情。可以使用任务链，通过组合偏函数来穿件新的函数，还可以把任务链
#  互相嵌套组合，如下所示：
#  >>> func = (multiply.s(10) | multiply.s(2))
#  >>> result = func.delay(16)
#  >>> result.get()
#  320

#  任务链可以嵌套：
#  >>> func = (
#  ...     multiply.s(10) | multiply.s(2) | (multiply.s(4) | multiply.s(5))
#  ... )
#  >>> result = func.delay(16)
#  >>> result.get()

#  复合任务：
#  复合任务（chord）函数生成了一个任务签名时，会先执行一个任务组，然后把最终结果传给回调函数：
#  >>> from celery import chord
#  >>> sig = chord(
#  >>>     group(multiply.s(i, i + 5) for i in range(10)),
#  >>>     log.s()
#  >>> )
#  >>> result = sig.delay()
#  >>> result.get()
#  [0, 6, 14, 24, 36, 50, 66, 84, 104, 126]
#  跟 lin 参数一样，这里的回调函数不会把结果返回给 get 方法

#  如果使用任务链的语法，把一个任务组和一个回调函数组合在一起，那么会自动生成一个
#  复合任务的签名：
#  sig = (group(multiply.s(i, i + 5) for i in range(10)) | log.s())
#  result = sig.delay()
#  result.get()
#  [0, 6, 14, 24, 36, 50, 66, 84, 104, 126]
