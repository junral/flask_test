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


将代码部署在 Heroku 服务器上：
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
