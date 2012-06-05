from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from models import *
import re

def get_python_dict_for_reqs(requirement_groups):
    req_groups = {}
    for group in requirement_groups:
        req_group_info = {}
        req_group_info['num_reqs_to_fulfill'] = group.n_prereqs
        reqs = {}
        for req in group.requirement_set.all():
            req_info = {}
            req_info['num_courses_to_fulfill'] = req.n_class
            req_info['bypassable'] = req.bypassable
            fulfillers = []
            for course in Course.objects.filter(tags=req.fulfillers):
                fulfillers.append(course.identifier)
            req_info['fulfillers'] = fulfillers
            reqs[req.name] = req_info
        req_group_info['requirements'] = reqs
        req_groups[group.name] = req_group_info
    return req_groups
    
@ensure_csrf_cookie
def index(request):
    plan = Plan.objects.all()[0]
    enrolled = Enrollment.objects.filter(plan=plan)
    exempt = []
    for course in plan.aps.all():
        requirement_groups = RequirementGroup.objects.filter(requirement__fulfillers__in=course.tags.all()) 
        requirements = Requirement.objects.filter(fulfillers__in=course.tags.all()) 
        setattr(course, 'req_groups', serializers.serialize('json', requirement_groups))
        print 'req_groups:'
        print course.req_groups
        print '----------------'
        setattr(course, 'reqs', serializers.serialize('json', requirements))
        print 'reqs:'
        print course.reqs
        print '----------------'
        exempt.append(course)
    
    args = {}
    args['plan'] = plan
    args['exempt'] = exempt
    args['allPlans'] = Plan.objects.all() # TODO only current user's plans
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
                requirement_groups = RequirementGroup.objects.filter(requirement__fulfillers__in=course.tags.all()) 
                requirements = Requirement.objects.filter(fulfillers__in=course.tags.all()) 
                setattr(course, 'start_time', e.course.start_time)
                setattr(course, 'end_time', e.course.end_time)
                setattr(course, 'weekdays', e.course.weekdays)
                setattr(course, 'units', e.units)
                setattr(course, 'req_groups', serializers.serialize('json', requirement_groups))
                setattr(course, 'reqs', serializers.serialize('json', requirements))
                prereq_groups = PrereqGroup.objects.filter(for_course=course)
                groups = []
                for group in prereq_groups:
                    satisfiers = []
                    for c in group.satisfiers.all():
                        satisfiers.append(c.identifier)
                    groups.append(satisfiers)
                setattr(course, 'prereq_groups', groups)                    
                    
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
                    if weekday == 'R' or weekday == 'H':
                        days.append(start_day + 3)
                    if weekday == 'F':
                        days.append(start_day + 4)
                setattr(course, 'days', days)
                course_offerings = CourseOffering.objects.filter(course=course).exclude(term__num=3) #kludge to exclude summer
                setattr(course, 'offering_json', simplejson.dumps(serializers.serialize('json', course_offerings, use_natural_keys=True)))
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
        
    major_req_groups = get_python_dict_for_reqs(RequirementGroup.objects.filter(major=plan.major))
    general_req_groups = get_python_dict_for_reqs(RequirementGroup.objects.filter(major__isnull=True))
            
    args['years'] = years
    args['totalUnits'] = totalUnits
    args['minUnits'] = plan.university.min_units
    args['offerings'] = offerings
    args['term_names'] = term_names
    args['max_units'] = plan.university.max_units_per_quarter
    args['general_reqs'] = simplejson.dumps(general_req_groups)
    args['major_reqs'] = simplejson.dumps(major_req_groups)
    return render_to_response('planner/index.html', args, context_instance=RequestContext(request))

def fill_response_info_for_courses(results, responseData):
    classNames = []
    offerings = {}
    prereq_groups = {}
    requirement_groups = {}
    requirements = {}
    for course in results:
        classNames.append(course.identifier)
        course_offerings = CourseOffering.objects.filter(course=course).exclude(term__num=3).order_by('year', 'term', 'start_time')
        offerings[course.identifier] = serializers.serialize('json', course_offerings, use_natural_keys=True)
        req_groups = RequirementGroup.objects.filter(requirement__fulfillers__in=course.tags.all())
        requirement_groups[course.identifier] = serializers.serialize('json', req_groups)
        reqs = Requirement.objects.filter(fulfillers__in=course.tags.all()) 
        requirements[course.identifier] = serializers.serialize('json', reqs)
        course_prereqs = []
        for group in PrereqGroup.objects.filter(for_course=course):
            satisfiers = []
            for c in group.satisfiers.all():
                satisfiers.append(c.identifier)
            course_prereqs.append(satisfiers)
        prereq_groups[course.identifier] = course_prereqs
        
    data = serializers.serialize('json', results)
    responseData["classes"] = data
    responseData["classNames"] = classNames
    responseData["offerings"] = offerings
    responseData["prereq_groups"] = prereq_groups
    responseData["req_groups"] = requirement_groups
    responseData["reqs"] = requirements
    return HttpResponse(simplejson.dumps(responseData), mimetype='application/json')
    

NUM_RESULTS = 10
    
def search(request, prefix, offset='0'):
    offset = int(offset)
    responseData = {}
    responseData["query"] = prefix
    responseData["numResults"] = Course.objects.filter(identifier__startswith=prefix).count()
    results = Course.objects.filter(identifier__startswith=prefix).order_by('dept', 'code', 'identifier')[offset:offset + NUM_RESULTS]
    if len(results) == 0:
        prefix = prefix.replace(' ', '')
        responseData["numResults"] = Course.objects.filter(identifier__startswith=prefix).count()
        results = Course.objects.filter(identifier__startswith=prefix).order_by('dept', 'code', 'identifier')[offset:offset + NUM_RESULTS]
    return fill_response_info_for_courses(results, responseData)
    
def course_info(request):
    course_names = request.POST.getlist('courseNames[]')
    responseData = {}
    responseData["query"] = course_names
    results = []
    for identifier in course_names:
        results.extend(Course.objects.filter(identifier=identifier))
    return fill_response_info_for_courses(results, responseData)

def req_search(request, requirement_name, offset='0'):
    offset = int(offset)
    responseData = {}
    responseData["query"] = requirement_name
    print requirement_name
    reqs = Requirement.objects.filter(name=requirement_name)
    results = []
    if len(reqs) == 1:
        responseData["numResults"] = Course.objects.filter(tags=reqs[0].fulfillers).count()
        results = Course.objects.filter(tags=reqs[0].fulfillers).order_by('dept', 'code', 'identifier')[offset:offset + NUM_RESULTS]
    print results
    return fill_response_info_for_courses(results, responseData) 
    

def add_course(request):
    params = request.POST.dict()
    course_name = params['course']
    year_num = params['year']
    term_num = params['term']
    plan_name = params['plan']
    units = params['units']
    offerings = CourseOffering.objects.filter(course__identifier=course_name, year=year_num, term=term_num)
    if len(offerings) > 0:
        to_add = offerings[0]
        # TODO correct Plan lookup
        plan = Plan.objects.filter(name=plan_name)[0]
        enrollment = Enrollment(course=to_add, plan=plan, units=units)
        enrollment.save()
    
    return HttpResponse()
    
def delete_course(request):
    params = request.POST.dict()
    course_name = params['course']
    year_num = params['year']
    term_num = params['term']
    plan_name = params['plan']
    # TODO correct plan lookup
    enrollments = Enrollment.objects.filter(course__course__identifier=course_name, course__year=year_num, course__term=term_num, plan__name=plan_name)
    if len(enrollments) == 1:
        to_delete = enrollments[0]
        to_delete.delete()
    else:
        print "wtf..."
    return HttpResponse()

def move_course(request):
    params = request.POST.dict()
    course_name = params['course']
    old_year = params['old_year']
    old_term = params['old_term']
    new_year = params['new_year']
    new_term = params['new_term']
    plan_name = params['plan']
    enrollments = Enrollment.objects.filter(course__course__identifier=course_name, course__year=old_year, course__term=old_term, plan__name=plan_name)
    if len(enrollments) == 1:
        to_switch = enrollments[0]
        offerings = CourseOffering.objects.filter(course__identifier=course_name, year=new_year, term=new_term)
        if len(offerings) > 0:
            offering = offerings[0]
            # TODO correct Plan lookup
            plan = Plan.objects.filter(name=plan_name)[0]
            to_switch.course = offering
            to_switch.save()
        
    return HttpResponse()

def set_exemption(request):
    params = request.POST.dict()
    identifier = params['course']
    plan_name = params['plan']
    add = params['add']
    courses = Course.objects.filter(identifier=identifier)
    if len(courses) == 1:
        course = courses[0]
        # TODO correct Plan lookup
        plan = Plan.objects.filter(name=plan_name)[0]
        if add == 'true':
            plan.aps.add(course)
        else:
            print "removing..."
            plan.aps.remove(course)
        plan.save()
        
    return HttpResponse()
    
    