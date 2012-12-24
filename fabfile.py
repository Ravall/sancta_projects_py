# -*- coding: utf-8 -*-
from fabric.api import *

env.activate = 'source /home/envs/admin_sancta/bin/activate'
env.hosts = ['root@78.47.157.221']

def deploy(tag=None):
    if not tag:
        print "для выкладки нужен тег"
    print "выкладываем тег {0}".format(tag)
    with cd('/home/web/django_admin'):
        with prefix(env.activate):
            run("git fetch")
            run("git remote prune origin")
            run("git checkout {0}".format(tag))
            run("cat release")
            run("pip install -r files/pip.freeze")
            run("python sancta/manage.py syncdb  --settings=config.admin")
            run("python sancta/manage.py migrate --settings=config.admin")
            run("python sancta/manage.py collectstatic  --settings=config.admin")
            run('service nginx stop')
            run('service nginx start')
            run('service uwsgi stop')
            run('service uwsgi start')
            run('service celeryd stop')
            run('service celeryd start')
            run("ps aux | grep 'celery'")
