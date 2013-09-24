from django import forms
from django.template import Context, loader

from Apps.subscribe.models import Member, Activation


# форма подписки на новости

ACTIONS = (
    (1, 'Подписаться'),
    (0, 'Отписаться'),
)

class SubscribeForm(forms.Form):
    email = forms.EmailField(label='Email')
    action = forms.ChoiceField(label='Действие', choices=ACTIONS)
     
    def clean(self):
        action = self.cleaned_data.get('action', None)
        email = self.cleaned_data.get('email', None)
        
        if email is None or action is None:
            return self.cleaned_data
        
        try:            
            member = Member.objects.get(email=email)
            if action == '1':
                raise forms.ValidationError, u'Пользователь c таким адресом уже зарегистрирован'           
        except Member.DoesNotExist:
            if action == '0':
                raise forms.ValidationError, u'Пользователя c таким адресом не существует'
        return self.cleaned_data
        
        
    def save(self):
        action = int(self.cleaned_data.get('action'))
        email = self.cleaned_data.get('email')
        
        if action:
            member = Member(email=email, is_active=0)
            template = 'emails/subscribe.html'
            subject = u'Подтверждение подписки на новости'
            member.save()
        else:
            member = Member.objects.get(email=email)
            subject = u'Отказ от подписки на новости'
            template = 'emails/unsubscribe.html'
            
        # Если уже существует ключ, удаляем его
        
        try:
            activation = Activation.objects.get(user=member)
            activation.delete()
        except Activation.DoesNotExist:
            pass

        activation = Activation(user=member, action=action)
        activation.save()        
        
        t = loader.get_template(template)
        c = {'code': activation.key}
        
        from django.core.mail import send_mail
        try:
            send_mail(subject, t.render(Context(c)), 'noreply@mk.mk.ua', [member.email], fail_silently=True)
        except:
            pass
            