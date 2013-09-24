from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from captcha.fields import CaptchaField
from Apps.news.models import Rubric
from Apps.news.models import Comment as NewsComment
from photoreport.models import Comment as ReportComment


# форма контактов

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField(label='Код')
    
    def submit(self):
        from django.core.mail import send_mail
        send_mail(u'Сообщение с сайта', self.cleaned_data['text'], 
            '%s <%s>' % (self.cleaned_data['name'], self.cleaned_data['email']), 
            ['kontakt.mk@gmail.com'], fail_silently=True)

# форма комментариев

class CommentFormNews(forms.ModelForm):
    captcha = CaptchaField(label='Код')

    class Meta:
        model = NewsComment
        exclude = ['pub_date', 'news']

# форма комментариев

class CommentFormReport(forms.ModelForm):
    captcha = CaptchaField(label='Код')

    class Meta:
        model = ReportComment
        exclude = ['pub_date', 'report']        
        
# форма поиска

class AuthorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()

search_widget = forms.widgets.TextInput(attrs={'class':"search_input"})
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=search_widget)
    rubric = forms.ModelChoiceField(Rubric.objects, required=False)
    author = AuthorChoiceField(User.objects, required=False)
    date_from = forms.DateField(required=False, input_formats=['%d.%m.%Y', '%d/%m/%Y'])
    date_to = forms.DateField(required=False, input_formats=['%d.%m.%Y', '%d/%m/%Y'])
    
    def search(self, objects):
        if self.cleaned_data.get('rubric', None):
            objects = objects.filter(rubric__exact=self.cleaned_data.get('rubric'))
        if self.cleaned_data.get('author', None):
            objects = objects.filter(author__exact=self.cleaned_data.get('author'))

        if self.cleaned_data.get('date_from', None):
            objects = objects.filter(pub_date__gte=self.cleaned_data.get('date_from'))

        if self.cleaned_data.get('date_to', None):
            date = self.cleaned_data.get('date_to')
            newdate = datetime(date.year, date.month, date.day, 23,59,59)
            objects = objects.filter(pub_date__lte=newdate)

        if self.cleaned_data.get('query', None):            
            objects = objects.filter(Q(title__contains=self.cleaned_data.get('query', None))
                | Q(text_middle__icontains=self.cleaned_data.get('query', None))
                | Q(text_big__icontains=self.cleaned_data.get('query', None)) )
        return objects.order_by('-pub_date')
	