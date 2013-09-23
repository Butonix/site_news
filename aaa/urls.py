from django.conf.urls.defaults import patterns, include, url
#from news.sitemaps import sitemaps
#from news.models import News, Photo

urlpatterns = patterns('',
    url(r'^$', 'news.views.index'),
    url(r'^rubric/(?P<slug>[A-z]+)/$', 'news.views.rubric'),
    url(r'^rubric/(?P<slug>[A-z]+)/\d{4}/\d{2}/\d{2}/(?P<id>\d{5})/$', 'news.views.news_detail'),
    url(r'^photo/extra/(?P<id>\d+)/$', 'news.views.photo', {'model':'extra'}),
    url(r'^photo/news/(?P<id>\d+)/$', 'news.views.photo', {'model':'news'}),
    url(r'^photo/report/(?P<id>\d+)/$', 'news.views.photo', {'model':'report'}),
    url(r'^photo/report/image/(?P<id>\d+)/$', 'news.views.photo', {'model':'report_photo'}),
    url(r'^search/$', 'news.views.search'),
#    url(r'^currency/$', 'news.views.currency'),
#    url(r'^fuel/$', 'news.views.fuel'),
    url(r'^playbill/$', 'news.views.playbill'),
    url(r'^playbill/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'news.views.playbill'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^subscribe/$', 'news.views.subscribe'),
    url(r'^subscribe/activation/(?P<key>\w+)/$', 'news.views.activation'),
    url(r'^contacts/$', 'news.views.contacts'),
    url(r'^advertising/$', 'news.views.adver'),
    url(r'^photoreport/$', 'news.views.photoreport_list'),
    url(r'^photoreport/\d{4}/\d{2}/\d{2}/(?P<id>\d{5})/$', 'news.views.photoreport', ),
    url(r'^ntdtv/$', 'news.views.ntdtv', ),
    url(r'^change_count/$', 'news.views.change_count', ),
)

from news.feeds import NewsFeed, YandexFeed
#feed_dict = {'latest':NewsFeed, 'yandex':YandexFeed, }

from django.views.decorators.cache import cache_page

urlpatterns += patterns('',
    url(r'^feeds/latest/$', cache_page(NewsFeed(), 60 * 30, ), ),
    url(r'^feeds/yandex/$', cache_page(YandexFeed(), 60 * 30, ), ),
#    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.Feed', {'feed_dict': feed_dict}),
#    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.Feed', {'feed_dict': feed_dict}),
)

from news.models import News
info_dict = {'queryset': News.objects.all(), 'date_field': 'pub_date', 'lastmod': 'pub_date', }

from django.contrib.sitemaps import GenericSitemap
sitemaps = {'news': GenericSitemap(info_dict, priority=0.04, changefreq='monthly', ), }

from django.contrib.sitemaps.views import sitemap

#import os

#from django.conf.urls.defaults import url, patterns
#from django.http import HttpResponse, Http404

#from static_sitemaps import conf

#def serve_index(request):
#    path = os.path.join(conf.ROOT_DIR, 'sitemap.xml')
#    if not os.path.exists(path):
#        raise Http404('No sitemap index file found on %r. Run django-admin.py '
#                      'refresh_sitemap first.' % path)
#    f = open(path)
#    content = f.readlines()
#    f.close()
#    return HttpResponse(content, mimetype='application/xml')

#urlpatterns += patterns('',
#    url(r'^sitemap\.xml$', serve_index, name='static_sitemaps_index'),
#)

#urlpatterns += patterns('',
#        url(r'^sitemap\.xml', include('static_sitemaps.urls', ), ),
#)

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', cache_page(sitemap, 60 * 60 * 24, ), {'sitemaps': sitemaps}, name='static_sitemaps_index', ),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}, name='sitemap', ),
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'mk_mk_mk_ua.views.home', name='home'),
    # url(r'^mk_mk_mk_ua/', include('mk_mk_mk_ua.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
