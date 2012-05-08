from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from models import *

def index(request):
    plan = Plan.objects.filter(student_name='Dan Vinegrad')[0]
    enrolled = Enrollment.objects.filter(plan=plan)
    
    args = {}
    years = [{}, {}, {}, {}]
    years[0]['year'] = '2012-2013'
    years[0]['name'] = 'Freshman'
    years[1]['year'] = '2013-2014'
    years[1]['name'] = 'Sophomore'
    years[2]['year'] = '2014-2015'
    years[2]['name'] = 'Junior'
    years[3]['year'] = '2015-2016'
    years[3]['name'] = 'Senior'
    
    totalUnits = 0
    start = plan.start_year.start_num
    for i in range(start,start + 4):
        year_num = i - start
        year = Year.objects.filter(start_num=i)[0]
        years[year_num]['year'] = year.__unicode__()
        year_enrolled = enrolled.filter(year=year)
        terms = [{}, {}, {}]
        for t in range(3):
            term = Term.objects.filter(num=t)[0]
            term_enrolled = year_enrolled.filter(term=term)
            terms[t]['courses'] = []
            for e in term_enrolled:
                course = e.course.course
                setattr(course, 'start_time', e.course.start_time)
                setattr(course, 'end_time', e.course.end_time)
                setattr(course, 'weekdays', e.course.weekdays)
                terms[t]['courses'].append(course)
                
            terms[t]['name'] = term.__unicode__() + years[year_num]['year']
            terms[t]['condensedName'] = terms[t]['name'].replace(' ', '')
            units = 0
            for course in terms[t]['courses']:
                setattr(course, 'condensedID', course.identifier.replace(' ', ''))
                units += course.units
                days = []
                start_day = 23
                for weekday in course.weekdays:
                    if weekday == 'M':
                        days.append(start_day)
                    if weekday == 'T':
                        days.append(start_day + 1)
                    if weekday == 'W':
                        days.append(start_day + 2)
                    if weekday == 'R':
                        days.append(start_day + 3)
                    if weekday == 'F':
                        days.append(start_day + 4)
                setattr(course, 'days', days)
            terms[t]['units'] = units
            totalUnits += units
        years[year_num]['terms'] = terms
            
    
    
    
    
    # for i in range(4):
    #     terms = [{}, {}, {}]
    #     terms[0]['courses'] = []
    #     terms[0]['name'] = 'Autumn ' + years[i]['year']
    #     terms[0]['condensedName'] = terms[0]['name'].replace(' ','')
    #     terms[1]['courses'] = []
    #     terms[1]['name'] = 'Winter ' + years[i]['year']
    #     terms[1]['condensedName'] = terms[1]['name'].replace(' ','')
    #     terms[2]['courses'] = []
    #     terms[2]['name'] = 'Spring ' + years[i]['year']
    #     terms[2]['condensedName'] = terms[2]['name'].replace(' ','')
    #     terms[0]['courses'].append(Course.objects.filter(identifier='CS 106A')[0])
    #     terms[0]['courses'].append(Course.objects.filter(identifier='Chem 31A')[0])
    #     terms[0]['courses'].append(Course.objects.filter(identifier='Econ 1A')[0])
    #     terms[1]['courses'].append(Course.objects.filter(identifier='PWR 1')[0])
    #     terms[1]['courses'].append(Course.objects.filter(identifier='Econ 1B')[0])
    #     terms[2]['courses'].append(Course.objects.filter(identifier='CS 106B')[0])
    #     terms[2]['courses'].append(Course.objects.filter(identifier='CS 103')[0])
    #     terms[2]['courses'].append(Course.objects.filter(identifier='Physics 41')[0])
    # 
    #     for term in terms:
    #         units = 0
    #         for course in term['courses']:
    #             setattr(course, 'condensedID', course.identifier.replace(' ', ''))
    #             units += course.units
    #             days = []
    #             start = 23
    #             for weekday in course.weekdays:
    #                 if weekday == 'M':
    #                     days.append(start)
    #                 if weekday == 'T':
    #                     days.append(start + 1)
    #                 if weekday == 'W':
    #                     days.append(start + 2)
    #                 if weekday == 'R':
    #                     days.append(start + 3)
    #                 if weekday == 'F':
    #                     days.append(start + 4)
    #             setattr(course, 'days', days)
    #                     
    #                     
    #         term['units'] = units
    #         totalUnits += units
    #     years[i]['terms'] = terms
            
    args['years'] = years
    args['totalUnits'] = totalUnits
    return render_to_response('planner/index.html', args, context_instance=RequestContext(request))
    
def search(request, prefix):
    responseData = {}
    results = Course.objects.filter(identifier__startswith=prefix).order_by('identifier')
    classNames = []
    for course in results:
        classNames.append(course.identifier)
    data = serializers.serialize('json', results)
    responseData["classes"] = data
    responseData["classNames"] = classNames
    return HttpResponse(simplejson.dumps(responseData), mimetype='application/json')
    