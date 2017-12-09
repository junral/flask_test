#!/usr/bin/env python
# coding: utf-8

from fabric.api import (
    env,
    local,
    run,
    sudo,
    cd
)


def test():
    local('python -m unittest discover')


def upgrade_libs():
    sudo('apt-get update')
    sudo('apt-get upgrade')


def setup():
    test()
    upgrade_libs()

    # 安装很多必备的 Python 库
    lib_list = [
        'build-essential',
        'git',
        'python',
        'python-pip',
        'python-all-dev',
        # 如果使用 supervisor 部署
        'supervisor',
        # 如果要使用 Nginx
        'nginx',
        # 如果使用 Apache
        'apache2',
        'libapache2-mod-proxy-uwsgi'
    ]
    for lib in lib_list:
        sudo('apt-get install -y {}')

    run('useradd -d /home/deploy/ deploy')
    run('gpasswd -a deploy sudo')

    # 允许 deploy 用户安装 Python 包
    sudo('chown -R deploy /usr/local/')

    # Python3
    sudo('chown -R deploy /usr/lib/python3.5/')
    # Python2
    # sudo('chown -R deploy /usr/lib/python2.7/')

    run('git config --global credential.helper store')

    with cd('/home/deploy'):
        run('git clone (your repo URL)')

    with cd('home/deploy/webapp'):
        run('pip install -r requirements.txt')
        run('python manage.py createdb')

def deploy():
    test()
    upgrade_libs()
    with cd('/home/deploy/webapp'):
        run('git pull')
        run('pip install -r requirements.txt')

        # if use supervisor to setup
        sudo('cp supervisord.conf /etc/supervisor/conf.d/webapp.conf')

        # if use Nginx
        sudo('cp nginx.conf /etc/nginx/sites-available/[your_domain]')
        sudo('ln -s /etc/nginx/sites-available/[your_domain] '
             '/etc/nginx/sites-enabled/[your_domain]')

        # if use Apache
        sudo('cp apache.conf '
             '/etc/apach2/site-avaliable/[your_domain]'
             )
        sudo('ln -sf /etc/apach2/site-avaliable/[your_domain]'
             '/etc/apach2/site-enabled/[your_domain]'
             )

    # restart the Apache service
    sudo('service apache2 restart')

    # restart the Nginx service
    sudo('service nginx restart')

    # restart supervisor service
    sudo('service supervisor restart')
