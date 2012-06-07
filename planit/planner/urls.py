from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('planner.views',
    url(r'^$', 'index'),
    url(r'^search/(?P<prefix>.+)/(?P<limit>\d+)/$', 'search'),
    url(r'^search/(?P<prefix>.+)/$', 'search', name='search'),
    url(r'^reqSearch/(?P<requirement_name>.+)/(?P<limit>\d+)/$', 'req_search'),
    url(r'^reqSearch/(?P<requirement_name>.+)/$', 'req_search', name='req_search'),
    url(r'^tracks/(?P<major_name>.+)/$', 'tracks_for_major', name='tracks'),
    url(r'^courseInfo/$', 'course_info', name='course_info'),
    url(r'^setExemption/$', 'set_exemption', name='exemption'),
    url(r'^addCourse/$', 'add_course'),
    url(r'^deleteCourse/$', 'delete_course'),
    url(r'^moveCourse/$', 'move_course'),
    url(r'^createPlan/$', 'create_plan'),
    url(r'^(?P<plan_name>.+)/$', 'index'),
)
