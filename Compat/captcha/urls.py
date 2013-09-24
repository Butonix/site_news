from django.conf.urls.defaults import *

urlpatterns = patterns('captcha.views',
    url(r'^(?P<filename>.*)/$', 'render', name='captcha_render'),
)