from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponseRedirect

from models import Rubric, News, Photo
from decorators import render_to
from tagging.models import TaggedItem
from Apps.news.forms import CommentFormReport, CommentFormNews, SearchForm, ContactForm
from subscribe.forms import SubscribeForm
from subscribe.models import Member, Activation
from other.models import Banner, Announce

#from gismeteo.models import Forecast
from photoreport.models import Report 
from photoreport.models import Photo as ReportPhoto
from playbill.models import Place, Type, Event
from datetime import date, timedelta


def context(request):
    path = '/'.join(request.path.split('/')[:3])
    if path[-1] != '/': 
        path = '%s/' % path
    
    from django.core.cache import cache
    # try to get product from cache
    banner_top = cache.get(u'baner_top', )
    # if a cache miss, fall back on db query
    if not banner_top:
        try:
            banner_top = Banner.objects.filter(place=1).order_by('-date')[0]
        except Banner.DoesNotExist:
 #           cache.delete(u'baner_top', )
            banner_top = None
        except IndexError:
#            cache.delete(u'baner_top', )
            banner_top = None
        # store item in cache for next time
        else:
            cache.set(u'baner_top', banner_top, 3600, ) # 1h

#    try: banner_top = Banner.objects.filter(place=1).order_by('-date')[0]
#    except: banner_top = None
    
#    total_sql = 0
#    for i in connection.queries:
#        total_sql += float(i['time'])
    
#    today = Forecast.objects.today()
#    if today:
#	if today.temperature_min > 0: today.temp_min = '+'+str(today.temperature_min)
#	else: today.temp_min = '-'+str(today.temperature_min)

#	if today.temperature_max > 0: today.temp_max = '+'+str(today.temperature_max)
#	else: today.temp_max = '-'+str(today.temperature_max)

#    tomorrow = Forecast.objects.tomorrow()
#    if tomorrow:
#	if tomorrow.temperature_min > 0: tomorrow.temp_min = '+'+str(tomorrow.temperature_min)
#	else: tomorrow.temp_min = '-'+str(tomorrow.temperature_min)

#	if tomorrow.temperature_min > 0: tomorrow.temp_max = '+'+str(tomorrow.temperature_max)
#	else: tomorrow.temp_max = '-'+str(tomorrow.temperature_max)

    # try to get product from cache
    rubrics = cache.get(u'rubrics', )
    # if a cache miss, fall back on db query
    if not rubrics:
        try:
            rubrics = Rubric.objects.order_by('-date')
        except Rubric.DoesNotExist:
            rubrics = None
        # store item in cache for next time
        else:
            cache.set(u'rubrics', rubrics, 86400, ) # 24h
#    'rubrics': Rubric.objects.order_by('-date'),
    # try to get product from cache
    newslist = cache.get(u'newslist', )
    # if a cache miss, fall back on db query
    if not newslist:
        try:
            newslist = News.objects.newslist(limit=20)
        except News.DoesNotExist:
            newslist = None
        # store item in cache for next time
        else:
            cache.set(u'newslist', newslist, 60, ) # 60sec
#    'newslist': News.objects.newslist(limit=20),
    # try to get product from cache
    popular_view = cache.get(u'popular_view', )
    # if a cache miss, fall back on db query
    if not popular_view:
        try:
            popular_view = News.objects.popular_view(limit=4)
        except News.DoesNotExist:
            popular_view = None
        # store item in cache for next time
        else:
            cache.set(u'popular_view', popular_view, 60, ) # 60sec * 15min
#    'popular_view': News.objects.popular_view(limit=4),
    # try to get product from cache
    popular_comment = cache.get(u'popular_comment', )
    # if a cache miss, fall back on db query
    if not popular_comment:
        try:
            popular_comment = News.objects.popular_comment(limit=4)
        except News.DoesNotExist:
            popular_comment = None
        # store item in cache for next time
        else:
            cache.set(u'popular_comment', popular_comment, 900, ) # 60sec * 15min
#    'popular_comment': News.objects.popular_comment(limit=4),
    return {
#        'rubrics': Rubric.objects.order_by('-date'),
        'rubrics': rubrics,
        'newslist': newslist,
        'popular_view': popular_view,
        'popular_comment': popular_comment,
        'page_url': path,
        'banner_top': banner_top,
        'announces': Announce.objects.order_by('-date'),
        'banner_right': Banner.objects.filter(place=2).order_by('-date'),
#        'weather_today': today,
#        'weather_tomorrow': tomorrow,
        'photoreports': Report.objects.filter(published=1).order_by('-pub_date')[:3],
#        'queries': connection.queries,
#        'total_sql': total_sql
    }

from django.shortcuts import render_to_response
from django.template import RequestContext
#@render_to('index.html')
def index(request, template_name='index.html', ):
#    return {
#        'first_locked': News.objects.first_locked(),
#        'rubric_locked': News.objects.rubric_locked(),
#    }
    return render_to_response(
        template_name,
		{
        'first_locked': News.objects.first_locked(),
        'rubric_locked': News.objects.rubric_locked(),
        },
        context_instance=RequestContext(request),
        )

@render_to('rubric.html')    
def rubric(request, slug):
    rubric = get_object_or_404(Rubric, slug=slug)
    return {
        'news': News.objects.published().filter(rubric=rubric).order_by('-rubric_locked', '-pub_date')[:20],
        'rubric': rubric
        }


#@render_to('news.html')
def news_detail(request, slug, id, template_name='news.html', ):
    news = get_object_or_404(News, pk=int(id), )
    tagged = TaggedItem.objects.get_related(news, News.objects.published())[:5]
    views_count = news.increase_view()

    if request.method == 'POST':        
        form = CommentFormNews(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.save()
            return HttpResponseRedirect(news.get_absolute_url())
    else:
        form = CommentFormNews()        
#    return {
#        'news': news, 
#        'tagged': tagged, 
#        'form':form
#    }
    return render_to_response(
        template_name,
        {
        'news': news, 
        'tagged': tagged, 
        'form':form,
		'views_count':views_count,
        },
        context_instance=RequestContext(request),
        )
    
@render_to('search.html')
def search(request):
    form = SearchForm(request.GET)
#    print form.errors
    if form.is_valid():
        news = form.search(News.objects)
    else:
        news = News.objects
    try:
        paginator = Paginator(news.all(), 5)
        pager = paginator.page(request.GET.get('page', 1))
    except InvalidPage:
        raise Http404

    return {
        'form':form,
        'pager':pager,
    }

#@render_to('currency.html')
#def currency(request):
#    from currency.models import Date
#    try:
#        date = Date.objects.select_related().latest('date')
#        exchange = date.exchange.select_related().all()
#        return {'date':date.date, 'exchange': exchange}
#    except:
#        return {}

#@render_to('fuel.html')
#def fuel(request):
#    from fuel.models import Date
#    try:
#        date = Date.objects.select_related().latest('date')
#        price = date.price.select_related().all()
#        return {'date':date.date, 'price': price}
#    except:
#        return {}

@render_to('playbill.html')
def playbill(request, year=date.today().year, month=date.today().month, day=date.today().day):

    today = date(int(year), int(month), int(day))
    
    if today < date.today():
        today = date.today()
    
    first_day_of_week = today - timedelta(today.weekday())
    calendar = ''
    
    for i in range(7):
        day = first_day_of_week + timedelta(i)
	class_name = ''	
	
	if i == 0: class_name = '_left'
	if i == 6: class_name = '_right'
	    
        if day < date.today(): calendar += '<td class="mk_calendar_digit%s_off">%s</td>' % (class_name, day.strftime('%d'))
        elif day == today: calendar += '<td class="mk_calendar_digit%s_on"><span class="mk_today">%s</span></td>' % (class_name, day.strftime('%d'))
        else: calendar += '<td class="mk_calendar_digit%s_on"><a href="/playbill/%s/">%s</a></td>' % (class_name, day.strftime('%Y/%m/%d'), day.strftime('%d'))
    
    next_week = first_day_of_week + timedelta(7)
    prev_week = first_day_of_week - timedelta(7)        
    
    events = Event.objects.filter(start_date__lte=today, end_date__gte=today).select_related().all()
    
    types = Type.objects.order_by('-add_date').all()
    for type in types:
        type.places = Event.objects.filter(place__type=type, start_date__lte=today, end_date__gte=today).select_related().order_by('-place__add_date').all()
    
    future = Event.objects.filter( 
            start_date__gte=today+timedelta(1), 
            start_date__lte=today+timedelta(21),
            allow_future=1).select_related().order_by('start_date').all()
    
    return {
        'types': types,
        'future': future,
        'today': today,
        'calendar': calendar,
        'next_week': next_week,
        'prev_week': prev_week,
        'page_url': '/playbill/',
    }
    
@render_to('photo.html')
def photo(request, id, model):    
    if model == 'news':
        obj = get_object_or_404(News, pk=id)
        photo = obj.photo
        sign = obj.photo_sign        
    elif model == 'extra':
        obj = get_object_or_404(Photo, pk=id)
        photo = obj.image
        sign = obj.sign
    elif model == 'report':
        obj = get_object_or_404(Report, pk=id)
        photo = obj.photo
        sign = obj.title
    elif model == 'report_photo':
        obj = get_object_or_404(ReportPhoto, pk=id)
        photo = obj.photo
        sign = obj.text
        
    return {'sign':sign, 'photo':photo}


@render_to('subscribe.html')    
def subscribe(request):
    success = request.GET.get('success', None)
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/subscribe/?success=1')
    else:
        form = SubscribeForm()
    return {'form':form, 'success':success}

def activation(request, key):    
    code = get_object_or_404(Activation, key=key)
    if code.action == 1:
        code.user.is_active = True
        code.user.save()
        code.delete()
        return HttpResponseRedirect('/subscribe/?success=2')
    else:
        code.user.delete()
        code.delete()
        return HttpResponseRedirect('/subscribe/?success=3')

@render_to('contacts.html')
def contacts(request):
    sended = 0
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sended = 1
            form.submit()
    else:
        form = ContactForm()
        print form
    return {'form':form, 'sended':sended}    

@render_to('adver.html')    
def adver(request):
    return {}
    
@render_to('photoreport_list.html')
def photoreport_list(request):
    return {'reports': Report.objects.filter(published=1).order_by('-pub_date')}

@render_to('photoreport.html')
def photoreport(request, id):
    report = get_object_or_404(Report, pk=id, published=1)
    tagged = TaggedItem.objects.get_related(report, Report.objects.filter(published=1))[:5]
    report.increase_view()
    
    if request.method == 'POST':        
        form = CommentFormReport(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.report = report
            comment.save()
            return HttpResponseRedirect(report.get_absolute_url())            
    else:
        form = CommentFormReport() 
    return {'report':report, 'tagged':tagged, 'form':form}

@render_to('ntdtv.html')
def ntdtv(request):#, slug, id):
    return {
        'popular_view': News.objects.popular_view(limit=5),
        'popular_comment': News.objects.popular_comment(limit=5),
    }

def change_count(request, ):
    import datetime
    date_filter = datetime.date(2012, 9, 1)
    news = News.objects.filter(add_date__gte=date_filter, )
    for each_news in news:
        each_news.update_comment_count()
#            obj = Counters.objects.get(news=each_news, )
#            obj.commets=each_news.comment_count
#            obj.save()
    return HttpResponseRedirect('/')