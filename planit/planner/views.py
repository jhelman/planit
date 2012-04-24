from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Course

def index(request):
    return render_to_response('planner/index.html', context_instance=RequestContext(request))