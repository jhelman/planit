from django.conf.urls import patterns, include, url
from name_reg import NameRegistrationForm

from django.views.generic.simple import direct_to_template
from registration.views import activate
from registration.views import register
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'planit.views.home', name='home'),
    # url(r'^planit/', include('planit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
   url(r'^accounts/activate/complete/$',
       direct_to_template,
       { 'template': 'registration/activation_complete.html' },
       name='registration_activation_complete'),
   url(r'^accounts/activate/(?P<activation_key>\w+)/$',
       activate,
       { 'backend': 'name_reg.NameBackend' },
       name='registration_activate'),
   url(r'^accounts/register/$',
       register,
       { 'backend': 'name_reg.NameBackend' },
       name='registration_register'),
   url(r'^accounts/register/complete/$',
       direct_to_template,
       { 'template': 'registration/registration_complete.html' },
       name='registration_complete'),
   url(r'^accounts/register/closed/$',
       direct_to_template,
       { 'template': 'registration/registration_closed.html' },
       name='registration_disallowed'),
    url(r'^accounts/logout/$', 'planner.views.logout'),
   (r'accounts', include('registration.auth_urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include('planner.urls')),
)
