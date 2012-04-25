from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Course

def index(request):
    args = {}
    years = [{}, {}, {}, {}]
    terms = [{}, {}, {}]
    terms[0]['courses'] = []
    terms[0]['name'] = 'Autumn 2011-2012'
    terms[0]['condensedName'] = terms[0]['name'].replace(' ','')
    terms[1]['courses'] = []
    terms[1]['name'] = 'Winter 2011-2012'
    terms[1]['condensedName'] = terms[1]['name'].replace(' ','')
    terms[2]['courses'] = []
    terms[2]['name'] = 'Spring 2011-2012'
    terms[2]['condensedName'] = terms[2]['name'].replace(' ','')
    terms[0]['courses'].append(Course.objects.filter(identifier='CS 106A')[0])
    terms[0]['courses'].append(Course.objects.filter(identifier='Chem 31A')[0])
    terms[0]['courses'].append(Course.objects.filter(identifier='Econ 1A')[0])
    terms[1]['courses'].append(Course.objects.filter(identifier='PWR 1')[0])
    terms[1]['courses'].append(Course.objects.filter(identifier='Econ 1B')[0])
    terms[2]['courses'].append(Course.objects.filter(identifier='CS 106B')[0])
    terms[2]['courses'].append(Course.objects.filter(identifier='CS 103')[0])
    terms[2]['courses'].append(Course.objects.filter(identifier='Physics 41')[0])

    for term in terms:
        for course in term['courses']:
            setattr(course, 'condensedID', course.identifier.replace(' ', ''))
    years[0]['year'] = '2011-2012'
    years[0]['name'] = 'Freshman'
    years[0]['terms'] = terms
    years[1]['year'] = '2012-2013'
    years[1]['name'] = 'Sophomore'
    years[1]['terms'] = terms
    years[2]['year'] = '2013-2014'
    years[2]['name'] = 'Junior'
    years[2]['terms'] = terms
    years[3]['year'] = '2014-2015'
    years[3]['name'] = 'Senior'
    years[3]['terms'] = terms
    args['terms'] = terms
    args['years'] = years
    return render_to_response('planner/index.html', args, context_instance=RequestContext(request))