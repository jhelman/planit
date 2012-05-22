from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('planner.views',
    url(r'^$', 'index'),
    url(r'^search/(?P<prefix>.+)/$', 'search', name='search'),
    url(r'^addCourse/$', 'add_course'),
    url(r'^deleteCourse/$', 'delete_course'),
    url(r'moveCourse/$', 'move_course'),
)
