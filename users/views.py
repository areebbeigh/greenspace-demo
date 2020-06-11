from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import Group
from django.conf import settings

from django_registration.views import RegistrationView as BaseRegistrationView

from users.forms import RegistrationForm


class RegistrationView(BaseRegistrationView):
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = '/'

    def register(self, form):
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['is_nursery_manager']:
                print('nursery manager field is true', form.fields['is_nursery_manager'])
                group = Group.objects.get(name=settings.NURSERY_MGR_GROUP)
                user.groups.add(group)
        else:
            self.form_invalid()
