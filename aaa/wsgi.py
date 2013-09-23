import os
#substitute mysite with the name of your project !!!
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/usr/www/projs/mk_mk_ua/'

#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
#
