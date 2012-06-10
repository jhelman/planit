from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail
from registration.backends.default import DefaultBackend


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'required' }


class NameRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(label=_(u'First Name'), max_length=30)
    last_name  = forms.CharField(label=_(u'Last Name'), max_length=30)

    def __init__(self, *args, **kwargs):
        super(NameRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['first_name', 'last_name', 'username', 
                                'email', 'password1', 'password2']

class NameBackend(DefaultBackend):
    def register(self, request, **kwargs):
        user = super(NameBackend, self).register(request, **kwargs)
        user.first_name = kwargs['first_name']        
        user.last_name = kwargs['last_name']
        user.save()
        
    def get_form_class(self, request):
        return NameRegistrationForm
