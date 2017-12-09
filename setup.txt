服务器部署应用方案：

fabfile.py
使用 farbric 把代码推送到服务器：
fabric 安装命令：
pip install fabric

使用 fabric 配置后的命令：
fabric setup
测试运行效果:
fabric test

使用 supervisor 运行 web 服务器
supervisor 安装命令：
apt-get -y install supervisor

1. gsever.py + fabfile.py + supervisord.conf
    使用 Gevent：
    启动和持续运行 Web 服务器，最简单的方式是使用 gevent 来托管应用。
    gevent 库使用协程（co-routines）并行地运行程序，gevent 具有运行
    WSGI 程序的接口，使用用简单且性能不错

    gevent 安装命令：
    pip install gevent

2. tserver.py + fabfile.py + supervisord.conf
    使用 Tornado：
    Tornado 是另一种非常简单的单纯用 Python 部署 WSGI 应用的方式，
    它是一种被设计用来处理多达数千并发连接请求的 Web 服务器，如果
    应用需要实时数据推送，则 Tornado 还支持通过 WebSocket 建立服务器
    的持续长连接

    Tornado：
    pip install tornado

3. 使用 wsgi.py + uwsgi.ini + nginx.conf + fabfile.py + supervisord.conf
    如果需要更强的性能或者定制化能力，则可以 Nginx + uWSGI 的 Python Web 应用
    部署方式，使用 Web 服务器 Nginx 作为前段，为 WSGI 服务器 uWSGI 提供反向
    代理服务。反向代理服务器是这样的程序：它们接收来自客户端的请求，并从真正
    的服务器哪里取得相应内容，再返回给客户端，就好像数据是由代理服务器提供给
    客户端一样

    uWSGI 的安装：
    pip install uwsgi

4. apache.conf + uwsgi.ini + wsgi.py + fabfile.py + supervisord.conf
    Apache httpd 和 Nginx 的配置过程基本相同。


将应用部署在 Heroku 服务器上：
Heroku 通过读取名为 Profile 的配置文件来运行服务，文件中包含一些命令，
并交给 Heroku 的容器（Heroku dyno 为服务器上运行的某种虚拟机）来执行

Heroku 登录命令：
heroku login

通过 foreman 命令可以在部署之前测试配置，以确认在 Heroku 上会正常工作
foreman start web

使用 create 命令创建一个容器，应用在 Heroku 服务器上就是由容器来执行的，
然后把代码 push 到 Git 仓库中 Heroku 的远程分支上
heroku create
git push heroku master

打开一个标签页来查看网站
heroku open

使用下面的命令安装 Heroku RabbitMQ 插件，选择免费套餐（叫作 lemur 套餐）：
heroku addons:create cloudamgqp:lemur

将应用部署到 AWS 服务器上：
登录地址：http://aws.amazon.ocm/elasticbenstalk
Elastic Beanstalk 是一个 Web 应用托管平台，为开发者提供了众多强大的特性，而开发者
无需担心任务服务器维护的问题。
在 Benstalk 使用 Apache 结合 mod_wsgi 连接 WSGI 应用。
在初始化的时候可以安装 ELastic Beanstalk 的命令行工具。这些工具能自动部署应用的新版本。
使用 pip 进行安装：
pip install awsebcli

配置命令行工具，在项目目录下运行下面的命令：
eb init

下面的命令可以查看在应用实例上运行了什么：
eb open

通过下面的命令部署应用：
eb deploy

在 Amazon Simple Queue Service 中使用 Celery：
为了使用 Celery，我们需要让 Elastic Beanstalk 实力在后台运行 Celery 工作进程，
还需要创建一个 Simple Queue Service（SQS）上的消息队列。需要安装一个帮助程序：
pip instal boto

然后需要把 CELERY_BROKER_URL 和 CELERY_backend_url 换成新的 URL，它会是下面这种形式：
sqs://aws_access_key_id:aws_secret_acces_key@

告诉 ELastic Beanstalk 在后台运行一个 Celery 工作进程。需要在项目根目录下创建一个
新的 .ebextensions 目录，然后在这个目录中放一个 .conf 文件。通过这个文具店，我们可以执行任意命令。
