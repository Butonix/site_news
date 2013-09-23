# coding=utf-8
# Django settings for mk_mk_mk_ua project.

import os
import sys

ROOT = os.path.dirname(__file__)
#sys.path.insert(0, os.path.join(ROOT, 'django'))
sys.path.insert(0, os.path.join(ROOT, 'apps'))
sys.path.insert(1, os.path.join(ROOT, 'compat'))
#sys.path.insert(3, ROOT)

DEBUG = False
#DEBUG = True
TEMPLATE_DEBUG = False
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('mk_mk_ua', 'sergey@chsz.biz'),
)

EMAIL_HOST = 'mail.chsz.biz'
EMAIL_HOST_USER = 'sergey@chsz.biz'
EMAIL_HOST_PASSWORD = 'warning123'

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    '.mk.mk.ua', # Allow domain and subdomains
    '.mk.mk.ua.', # Also allow FQDN and subdomains
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mk_mk_ua',           # Or path to database file if using sqlite3.
        'USER': 'root',           # Not used with sqlite3.
#        'USER': 'pgsql',           # Not used with sqlite3.
#        'USER': 'mk_mk_ua',           # Not used with sqlite3.
#        'PASSWORD': '', # Not used with sqlite3.
#        'PASSWORD': 'M53Z6Et8DxUGrVdD', # Not used with sqlite3.
        'PASSWORD': 'secret', # Not used with sqlite3.
#        'PASSWORD': 'secret', # Not used with sqlite3.
        'HOST': '192.168.1.12',       # Set to empty string for localhost. Not used with sqlite3.
#        'HOST': '/var/mysql.sock/mysql.sock', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',               # Set to empty string for default. Not used with sqlite3.
#        'PORT': '5432',               # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/usr/www/media/mk_mk_ua'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/' #

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+xqz=l=hwls3kf=*t+_lzr_w555&mwzzwr=qx&5k00+&9-8c&g'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
##     'django.template.loaders.eggs.Loader',
#)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'news.views.context',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '127.0.0.1:11211',
#            '172.19.26.240:11211',
#            '172.19.26.242:11211',
#            '172.19.26.244:11213',
#            'LOCATION': 'unix:/tmp/memcached.sock',
        ]
    }
}
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
##        'LOCATION': 'unique-snowflake'
#    }
#}

MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.CacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.middleware.gzip.GZipMiddleware',
#    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    '/usr/www/projs/mk_mk_ua/template',
#    os.path.join(ROOT, 'template'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#from news.models import News
#info_dict = {'queryset': News.objects.all(), 'date_field': 'pub_date', }

#from django.contrib.sitemaps import GenericSitemap
#sitemaps = {'news': GenericSitemap(info_dict, priority=0.06, changefreq='monthly', ), }

#from django.views.decorators.cache import cache_page
#from django.contrib.sitemaps.views import sitemap

#urlpatterns += patterns('',
#    url(r'^sitemap\.xml$', cache_page(sitemap, 60 * 60 * 24, ), {'sitemaps': sitemaps}, name='sitemap', ),
##    url(r'^sitemap\.xml$', cache_page(sitemap, 60 * 60 * 24, ), 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='sitemap', ),
#)

#STATICSITEMAPS_ROOT_SITEMAP = 'mk_mk_ua.urls.sitemaps'
#STATICSITEMAPS_ROOT_DIR = '/usr/www/media/mk_mk_ua'
#STATICSITEMAPS_USE_GZIP = True
#STATICSITEMAPS_PING_GOOGLE = False

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'other',
    'subscribe',
    'currency',
    'fuel',
    'news',
    'subscribe',
    'tagging',
#    'markup',
#    'gismeteo',
    'photoreport',
    'playbill',
    'django.contrib.sitemaps',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'debug_toolbar',
#    'static_sitemaps',
)

INTERNAL_IPS = ('127.0.0.1', '192.168.3.30', '193.33.237.146', '217.77.210.70', '46.33.244.34', )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'mail_admins': {
#            'level': 'ERROR',
#            'class': 'django.utils.log.AdminEmailHandler'
#        }
#    },
#    'loggers': {
#        'django.request': {
#            'handlers': ['mail_admins'],
#            'level': 'ERROR',
#            'propagate': True,
#        },
#    }
#}

DEBUG_TOOLBAR_PANELS = (
'debug_toolbar.panels.version.VersionDebugPanel',
'debug_toolbar.panels.timer.TimerDebugPanel',
'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
'debug_toolbar.panels.headers.HeaderDebugPanel',
'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
'debug_toolbar.panels.template.TemplateDebugPanel',
'debug_toolbar.panels.sql.SQLDebugPanel',
'debug_toolbar.panels.cache.CacheDebugPanel',
'debug_toolbar.panels.signals.SignalDebugPanel',
'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
'EXCLUDE_URLS': ('/admin/',), # не работает, но в разработке есть...
'INTERCEPT_REDIRECTS': False,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
