from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('planner.views',
    url(r'^$', 'index'),
    url(r'^search/(?P<prefix>.+)/$', 'search', name='search'),
    url(r'^req_search/(?P<requirement_name>.+)/$', 'req_search', name='req_search'),
    url(r'^setExemption/$', 'set_exemption', name='exemption'),
    url(r'^addCourse/$', 'add_course'),
    url(r'^deleteCourse/$', 'delete_course'),
    url(r'moveCourse/$', 'move_course'),
)
