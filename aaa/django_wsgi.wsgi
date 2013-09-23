import os
#substitute mysite with the name of your project !!!
os.environ['DJANGO_SETTINGS_MODULE'] = 'mk_mk_ua.settings'
os.environ['PYTHON_EGG_CACHE'] = '/usr/www/envs/mk_mk_ua'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()