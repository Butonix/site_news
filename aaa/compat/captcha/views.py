from django.http import HttpResponse
from captcha.fields import CaptchaField
from django import forms
from utils import Captcha

    
def render(request, filename):
    response = HttpResponse(mimetype='image/png')
    captcha = Captcha(filename)
    captcha.draw(response)        
    return response