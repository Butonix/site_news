# Django settings for untitled project.

DEBUG = False
#DEBUG = True
TEMPLATE_DEBUG = DEBUG
#TEMPLATE_DEBUG = DEBUG

#import os
#import sys

#ROOT = os.path.dirname(__file__)
##sys.path.insert(0, os.path.join(ROOT, 'django'))
#sys.path.insert(0, os.path.join(ROOT, 'apps'))
#sys.path.insert(1, os.path.join(ROOT, '../Compat'))
##sys.path.insert(3, ROOT)

import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )

ROOT = PROJECT_PATH

path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'site@keksik.com.ua'
EMAIL_HOST_PASSWORD = '1q2w3e4r'
#EMAIL_HOST = 'mail.chsz.biz'
#EMAIL_HOST_USER = 'sergey@chsz.biz'
#EMAIL_HOST_PASSWORD = 'warning123'

ADMINS = (
    ('mk_mk_ua', 'sergey@chsz.biz'),
#    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

SERVER = os.path.isfile(path('mk_mk_ua.server.key', ), )

if SERVER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mk_mk_ua',             # Or path to database file if using sqlite3.
            'USER': 'root',                 # Not used with sqlite3.
            'PASSWORD': 'secret',           # Not used with sqlite3.
            'HOST': '192.168.1.12',         # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                 # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': path('db/mk_mk_ua.sqlite3', ),  # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
#ALLOWED_HOSTS = []
ALLOWED_HOSTS = [
    'mk.mk.ua',  # Allow domain and subdomains
    '.mk.mk.ua',  # Allow domain and subdomains
    '.mk.mk.ua.',  # Also allow FQDN and subdomains
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/usr/www/media/mk_mk_ua'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
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
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!dx&82u*a=6&v*h83!=-y7&3m-d8jr9kll144frwb2@0g1v@*p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#    # 'django.template.loaders.eggs.Loader',
#)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'Apps.news.views.context',
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
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Project.wsgi.application'

TEMPLATE_DIRS = path('templates')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'Apps.news',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
