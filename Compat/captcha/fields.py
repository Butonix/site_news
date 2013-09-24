from django import forms
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.core.urlresolvers import reverse
from Compat.captcha.utils import Captcha


class ImageWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, src=value)
        return mark_safe(u'<img%s />' % flatatt(final_attrs))

        
class CaptchaWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (forms.TextInput(), ImageWidget(), forms.HiddenInput())
        super(CaptchaWidget, self).__init__(widgets, attrs)

    def format_output(self, widgets):
        return u'<table cellspacing="0" cellpadding="0"><tr><td>%s</td><td>%s%s</td></tr></table>' % \
                (widgets[0], widgets[1], widgets[2])
    
    def decompress(self, value):
        captcha = Captcha()
        url = reverse('captcha_render', args=[captcha.filename])
        return ('', url, captcha.filename)

    def render(self, name, value, attrs=None):
        return super(CaptchaWidget, self).render(name, None, attrs)

        
class CaptchaField(forms.Field):

    widget = CaptchaWidget

    def __init__(self, *args, **kwargs):
        super(CaptchaField, self).__init__(*args, **kwargs)
        self.label = kwargs.get('label', u'Проверка')
        self.help_text = kwargs.get('help_text', u'Введите символы на картинке')
        
    def clean(self, value):
        captcha = Captcha(value[2])
        if captcha.text is None:
            raise forms.ValidationError(u'Проверочное число устарело. Введите число еще раз')
        if captcha.text != value[0]:
            raise forms.ValidationError(u'Неправильный ответ')
        return value