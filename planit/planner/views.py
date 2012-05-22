from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from models import *
import re

def index(request):
    plan = Plan.objects.filter(student_name='Dan Vinegrad')[0]
    enrolled = Enrollment.objects.filter(plan=plan)
    
    args = {}
    args['plan'] = plan
    years = [{}, {}, {}, {}]
    years[0]['name'] = 'Freshman'
    years[1]['name'] = 'Sophomore'
    years[2]['name'] = 'Junior'
    years[3]['name'] = 'Senior'
    term_names = []
    
    totalUnits = 0
    start = plan.start_year
    for i in range(start,start + 4):
        year_num = i - start
        years[year_num]['year'] = str(i) + '-' + str(i + 1)
        years[year_num]['start_num'] = i
        years[year_num]['year_index'] = i - start
        year_enrolled = enrolled.filter(course__year=i)
        terms = [{}, {}, {}]
        for t in range(3):
            term = Term.objects.filter(num=t)[0]
            term_enrolled = year_enrolled.filter(course__term=term)
            terms[t]['courses'] = []
            for e in term_enrolled:
                course = e.course.course
                setattr(course, 'start_time', e.course.start_time)
                setattr(course, 'end_time', e.course.end_time)
                setattr(course, 'weekdays', e.course.weekdays)
                terms[t]['courses'].append(course)
                
            terms[t]['name'] = term.__unicode__() + years[year_num]['year']
            terms[t]['condensedName'] = terms[t]['name'].replace(' ', '')
            terms[t]['num'] = term.num
            term_name = term.__unicode__()
            if term_name not in term_names:
                term_names.append(term_name)
            units = 0
            for course in terms[t]['courses']:
                setattr(course, 'condensedID', course.identifier.replace(' ', ''))
                units += course.max_units
                days = []
                start_day = 23
                for weekday in course.weekdays:
                    if weekday == 'M':
                        days.append(start_day)
                    if weekday == 'T':
                        days.append(start_day + 1)
                    if weekday == 'W':
                        days.append(start_day + 2)
                    if weekday == 'R' or weekday == 'H':
                        days.append(start_day + 3)
                    if weekday == 'F':
                        days.append(start_day + 4)
                setattr(course, 'days', days)
                course_offerings = CourseOffering.objects.filter(course=course).exclude(term__num=3)
                setattr(course, 'offering_json', simplejson.dumps(serializers.serialize('json', course_offerings)))
                setattr(course, 'course_json', simplejson.dumps(serializers.serialize('json', [course])))
            terms[t]['units'] = units
            totalUnits += units
        years[year_num]['terms'] = terms
            
    offerings = {}
    for e in enrolled:
        course = e.course.course
        course_offerings = CourseOffering.objects.filter(course=course).exclude(term__num=3)
        offered_terms = []
        for offering in course_offerings:
            offered_terms.append((offering.term.num, offering.year))
        offerings[str(course.identifier)] = course_offerings
            
    args['years'] = years
    args['totalUnits'] = totalUnits
    args['offerings'] = offerings
    args['term_names'] = term_names
    args['max_units'] = plan.university.max_units_per_quarter
    print offerings
    return render_to_response('planner/index.html', args, context_instance=RequestContext(request))
    
def search(request, prefix):
    responseData = {}
    responseData["query"] = prefix
    results = Course.objects.filter(identifier__startswith=prefix).order_by('identifier')
    if len(results) == 0:
        prefix = prefix.replace(' ', '')
        results = Course.objects.filter(identifier__startswith=prefix).order_by('identifier')
    classNames = []
    offerings = {}
    for course in results:
        classNames.append(course.identifier)
        course_offerings = CourseOffering.objects.filter(course=course).exclude(term__num=3).order_by('year', 'term', 'start_time')
        offerings[course.identifier] = serializers.serialize('json', course_offerings)
        
    data = serializers.serialize('json', results)
    responseData["classes"] = data
    responseData["classNames"] = classNames
    responseData["offerings"] = offerings
    return HttpResponse(simplejson.dumps(responseData), mimetype='application/json')
    

def add_course(request):
    params = request.POST.dict()
    course_name = params['course']
    year_num = params['year']
    term_num = params['term']
    plan_name = params['plan']
    start_time = params['start']
    weekdays = params['weekdays']
    # TODO find the offering and add an enrollment for it
    return HttpResponse()
    
def delete_course(request):
    params = request.POST.dict()
    print params
    course_name = params['course']
    year_num = params['year']
    term_num = params['term']
    plan_name = params['plan']
    # TODO find the enrollment and delete it
    enrollments = Enrollment.objects.filter(course__course__identifier=course_name).filter(course__year=year_num).filter(course__term=term_num).filter(plan__student_name=plan_name)
    if (len(enrollments) == 1):
        to_delete = enrollments[0]
        to_delete.delete()
    else:
        print "wtf..."
    return HttpResponse()
    