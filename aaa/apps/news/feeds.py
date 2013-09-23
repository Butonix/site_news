# coding=utf-8
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Rss201rev2Feed
from models import News
import urllib

class NewsFeed(Feed):
    title = u'Лента новостей mk.mk.ua'
    link = 'http://www.mk.mk.ua/'
    description = 'Николаевские новости сайта http://www.mk.mk.ua/'

    def item_pubdate(self, item):
        return item.pub_date

    def item_extra_kwargs(self, item, ):
        return {
            'text_middle':item.text_middle,
            'text_big':item.text_big, }

    def items(self):
        return News.objects.newslist(limit=500, )

class YandexCustomFeed(Rss201rev2Feed):

    def rss_attributes(self):
        attrs = super(YandexCustomFeed, self).rss_attributes()
        attrs['xmlns:yandex'] = 'http://news.yandex.ru'
        return attrs

    def add_root_elements(self, handler):
        attrs = super(YandexCustomFeed, self).add_root_elements(handler)
        handler.startElement('image', attrs={})

        handler.startElement('url', attrs={})
        handler.characters('http://www.mk.mk.ua/static/images/mkmkua100px.gif')
        handler.endElement('url')

        handler.startElement('title', attrs={})
        handler.characters(YandexFeed.title)
        handler.endElement('title')

        handler.startElement('link', attrs={})
        handler.characters(YandexFeed.link)
        handler.endElement('link')

        handler.endElement('image')
        return attrs

    def add_item_elements(self, handler, item):
        super(YandexCustomFeed, self).add_item_elements(handler, item)
        full_text = u'%s\n%s' % (item['text_middle'], item['text_big'], )
        import markdown
        full_text_html = markdown.markdown(full_text)
        handler.addQuickElement('yandex:full-text', full_text_html, )

class YandexFeed(NewsFeed):
    feed_type = YandexCustomFeed
