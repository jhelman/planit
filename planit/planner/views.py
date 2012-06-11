from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from models import *
import re
from urllib import unquote
from django.contrib.auth import logout as dj_logout

def get_python_dict_for_reqs(requirement_groups):
    req_groups = {}
    for group in requirement_groups:
        req_group_info = {}
        req_group_info['num_reqs_to_fulfill'] = group.n_reqs
        reqs = {}
        for req in group.requirement_set.all():
            req_info = {}
            req_info['num_courses_to_fulfill'] = req.n_class
            req_info['bypassable'] = req.bypassable
            req_info['exclusive'] = req.exclusive
            fulfillers = []
            for course in Course.objects.filter(tags=req.fulfillers):
                fulfillers.append(course.identifier)
            req_info['fulfillers'] = fulfillers
            reqs[req.name] = req_info
        req_group_info['requirements'] = reqs
        req_groups[group.name] = req_group_info
    return req_groups
    
@ensure_csrf_cookie
def index(request, plan_name=None):
    user = None
    try:
        user = User.objects.filter(username=request.user)[0]
    except:
        return HttpResponseRedirect('/accounts/login')
    plan = None
    args = {}
    args['user'] = user
    args['allPlans'] = Plan.objects.filter(user=user)
    args['majors'] = simplejson.dumps(serializers.serialize('json', Major.objects.all(), use_natural_keys=True))
    try:
        if plan_name:
            plan = Plan.objects.filter(name=plan_name, user__username=request.user)[0]
        else:
            plan = Plan.objects.filter(user__username=request.user)[0]
    except:
        return render_to_response('planner/toolbar.html', args, context_instance=RequestContext(request))
    
    enrolled = Enrollment.objects.filter(plan=plan)
    exempt = []
    for exemption in plan.aps.all():
        course = exemption.course
        requirement_groups = RequirementGroup.objects.filter(requirement__fulfillers__in=course.tags.all()).distinct()
        requirements = Requirement.objects.filter(fulfillers__in=course.tags.all()).distinct()
        setattr(course, 'req_groups', serializers.serialize('json', requirement_groups))
        setattr(course, 'reqs', serializers.serialize('json', requirements))
        if exemption.mutex_req_fulfilled:
            setattr(course, 'mutex_req_fulfilled', serializers.serialize('json', [exemption.mutex_req_fulfilled], use_natural_keys=True))
        else:
            setattr(course, 'mutex_req_fulfilled', False)
        exempt.append(course)
    
    args['plan'] = plan
    args['exempt'] = exempt
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
                requirement_groups = RequirementGroup.objects.filter(requirement__fulfillers__in=course.tags.all()).distinct()
                requirements = Requirement.objects.filter(fulfillers__in=course.tags.all()).distinct()
                setattr(course, 'start_time', e.course.start_time)
                setattr(course, 'end_time', e.course.end_time)
                setattr(course, 'weekdays', e.course.weekdays)
                setattr(course, 'units', e.units)
                setattr(course, 'req_groups', serializers.serialize('json', requirement_groups))
                setattr(course, 'reqs', serializers.serialize('json', requirements))
                if e.mutex_req_fulfilled:
                    setattr(course, 'mutex_req_fulfilled', serializers.serialize('json', [e.mutex_req_fulfilled], use_natural_keys=True))
                else:
                    setattr(course, 'mutex_req_fulfilled', False)
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
        
    major_reqs = list(RequirementGroup.objects.filter(major=plan.major, is_track=False).distinct())
    major_reqs.extend(list(RequirementGroup.objects.filter(major=plan.major, is_track=True, name=plan.track).distinct()))
    major_req_groups = get_python_dict_for_reqs(major_reqs)
    general_req_groups = get_python_dict_for_reqs(RequirementGroup.objects.filter(major__isnull=True).distinct())
            
    args['years'] = years
    args['totalUnits'] = totalUnits
    args['minUnits'] = plan.university.min_units
    args['offerings'] = offerings
    args['term_names'] = term_names
    args['max_units'] = plan.university.max_units_per_quarter
    args['general_reqs'] = simplejson.dumps(general_req_groups)
    args['major_reqs'] = simplejson.dumps(major_req_groups)
    return render_to_response('planner/index.html', args, context_instance=RequestContext(request))

def fill_response_info_for_courses(results, response_data):
    classNames = []
    offerings = {}
    prereq_groups = {}
    requirement_groups = {}
    requirements = {}
    for course in results:
        classNames.append(course.identifier)
        course_offerings = CourseOffering.objects.filter(course=course).exclude(term__num=3).order_by('year', 'term', 'start_time')
        offerings[course.identifier] = serializers.serialize('json', course_offerings, use_natural_keys=True)
        req_groups = RequirementGroup.objects.filter(requirement__fulfillers__in=course.tags.all()).distinct()
        requirement_groups[course.identifier] = serializers.serialize('json', req_groups)
        reqs = Requirement.objects.filter(fulfillers__in=course.tags.all()).distinct()
        requirements[course.identifier] = serializers.serialize('json', reqs, use_natural_keys=True)
        course_prereqs = []
        for group in PrereqGroup.objects.filter(for_course=course):
            satisfiers = []
            for c in group.satisfiers.all():
                satisfiers.append(c.identifier)
            course_prereqs.append(satisfiers)
        prereq_groups[course.identifier] = course_prereqs
        
    data = serializers.serialize('json', results)
    response_data["classes"] = data
    response_data["classNames"] = classNames
    response_data["offerings"] = offerings
    response_data["prereq_groups"] = prereq_groups
    response_data["req_groups"] = requirement_groups
    response_data["reqs"] = requirements
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
    

NUM_RESULTS = 10
    
def search(request, prefix, limit='0'):
    prefix = unquote(prefix)
    limit = int(limit)
    response_data = {}
    response_data["query"] = prefix
    response_data["numResults"] = Course.objects.filter(identifier__startswith=prefix).count()
    if limit > 0:
        results = Course.objects.filter(identifier__startswith=prefix).order_by('dept', 'code', 'identifier')[:limit]
    else:
        results = Course.objects.filter(identifier__startswith=prefix).order_by('dept', 'code', 'identifier')
    if len(results) == 0:
        prefix = prefix.replace(' ', '')
        response_data["numResults"] = Course.objects.filter(identifier__startswith=prefix).count()
        if limit > 0:
            results = Course.objects.filter(identifier__startswith=prefix).order_by('dept', 'code', 'identifier')[:limit]
        else:
            results = Course.objects.filter(identifier__startswith=prefix).order_by('dept', 'code', 'identifier')
    return fill_response_info_for_courses(results, response_data)
    
def course_info(request):
    course_names = request.POST.getlist('courseNames[]')
    response_data = {}
    response_data["query"] = course_names
    results = []
    for identifier in course_names:
        results.extend(Course.objects.filter(identifier=identifier))
    return fill_response_info_for_courses(results, response_data)

def req_search(request, requirement_name, limit='0'):
    requirement_name = unquote(requirement_name)
    limit = int(limit)
    response_data = {}
    response_data["query"] = requirement_name
    reqs = Requirement.objects.filter(name=requirement_name).distinct()
    results = []
    if len(reqs) == 1:
        response_data["numResults"] = Course.objects.filter(tags=reqs[0].fulfillers).count()
        if limit > 0:
            results = Course.objects.filter(tags=reqs[0].fulfillers).order_by('dept', 'code', 'identifier')[:limit]
        else:
            results = Course.objects.filter(tags=reqs[0].fulfillers).order_by('dept', 'code', 'identifier')
    return fill_response_info_for_courses(results, response_data) 
    

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
        plan = Plan.objects.filter(name=plan_name, user__username=request.user)[0]
        enrollment = Enrollment(course=to_add, plan=plan, units=units)
        if 'mutexReq' in params:
            mutex_req = params['mutexReq']
            reqs = Requirement.objects.filter(name=mutex_req).distinct()
            if len(reqs) == 1:
                req = reqs[0]
                enrollment.mutex_req_fulfilled = req
        enrollment.save()
    
    return HttpResponse()
    
def delete_course(request):
    params = request.POST.dict()
    course_name = params['course']
    year_num = params['year']
    term_num = params['term']
    plan_name = params['plan']
    enrollments = Enrollment.objects.filter(course__course__identifier=course_name, course__year=year_num, course__term=term_num, plan__name=plan_name, plan__user__username=request.user)
    if len(enrollments) == 1:
        to_delete = enrollments[0]
        to_delete.delete()
    return HttpResponse()

def move_course(request):
    params = request.POST.dict()
    course_name = params['course']
    old_year = params['old_year']
    old_term = params['old_term']
    new_year = params['new_year']
    new_term = params['new_term']
    plan_name = params['plan']
    enrollments = Enrollment.objects.filter(course__course__identifier=course_name, course__year=old_year, course__term=old_term, plan__name=plan_name, plan__user__username=request.user)
    if len(enrollments) == 1:
        to_switch = enrollments[0]
        offerings = CourseOffering.objects.filter(course__identifier=course_name, year=new_year, term=new_term)
        if len(offerings) > 0:
            offering = offerings[0]
            plan = Plan.objects.filter(name=plan_name, user__username=request.user)[0]
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
        plan = Plan.objects.filter(name=plan_name, user__username=request.user)[0]
        if add == 'true':
            exemption = Exemption(course=course)
            if 'mutexReq' in params:
                mutex_req = params['mutexReq']
                reqs = Requirement.objects.filter(name=mutex_req).distinct()
                if len(reqs) == 1:
                    req = reqs[0]
                    exemption.mutex_req_fulfilled = req
            exemption.save()
            plan.aps.add(exemption)
        else:
            exemption = plan.aps.filter(course=course)[0]
            plan.aps.remove(exemption)
        plan.save()
        
    return HttpResponse()
    
def tracks_for_major(request, major_name):
    response_data = {}
    response_data["query"] = major_name
    track_names = []
    major = Major.objects.filter(name=major_name)[0]
    for track in major.tracks.all():
        track_names.append(track.name)
    response_data["tracks"] = track_names
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

@ensure_csrf_cookie
def create_plan(request):
    params = request.POST.dict()
    plan_name = params['planName']
    major_name = params['major']
    grad_year = params['gradYear']
    start_year = int(grad_year) - 4
    major = Major.objects.filter(name=major_name)[0]
    if 'track' in params:
        track_name = params['track']
        tracks = RequirementGroup.objects.filter(name=track_name, is_track=True, major=major).distinct()
    else:
        tracks = []
    univ = University.objects.filter(name='Stanford')[0]
    user = User.objects.filter(username=request.user)[0]
    plan = Plan(name=plan_name, user=user, university=univ, major=major, start_year=start_year, num_years=4)
    if len(tracks) == 1:
        plan.track = tracks[0]
    plan.save()
    return HttpResponseRedirect('/plan/' + plan_name + '/')



def check_plan_name(request, plan_name):
    user = User.objects.filter(username=request.user)[0]
    if Plan.objects.filter(user=user, name=plan_name).count() > 0:
        return HttpResponse("exists")
    else:
        return HttpResponse("does not exist")
    
def delete_plan(request):
    params = request.POST.dict()
    user = User.objects.filter(username=request.user)[0]
    plan_name = params['planName']
    plan = Plan.objects.filter(user=user, name=plan_name)
    plan.delete()
    return HttpResponse()

def edit_settings(request):
    params = request.POST.dict()
    user = User.objects.filter(username=request.user)[0]
    first_name = params['first']
    last_name = params['last']
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return HttpResponse()
    
def logout(request):
    dj_logout(request)
    return HttpResponseRedirect('/accounts/login')
