from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Course

def index(request):
    args = {}
    years = [{}, {}, {}, {}]
    years[0]['year'] = '2011-2012'
    years[0]['name'] = 'Freshman'
    years[1]['year'] = '2012-2013'
    years[1]['name'] = 'Sophomore'
    years[2]['year'] = '2013-2014'
    years[2]['name'] = 'Junior'
    years[3]['year'] = '2014-2015'
    years[3]['name'] = 'Senior'
    
    totalUnits = 0
    
    for i in range(4):
        terms = [{}, {}, {}]
        terms[0]['courses'] = []
        terms[0]['name'] = 'Autumn ' + years[i]['year']
        terms[0]['condensedName'] = terms[0]['name'].replace(' ','')
        terms[1]['courses'] = []
        terms[1]['name'] = 'Winter ' + years[i]['year']
        terms[1]['condensedName'] = terms[1]['name'].replace(' ','')
        terms[2]['courses'] = []
        terms[2]['name'] = 'Spring ' + years[i]['year']
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
            units = 0
            for course in term['courses']:
                setattr(course, 'condensedID', course.identifier.replace(' ', ''))
                units += course.units
                days = []
                start = 23
                for weekday in course.weekdays:
                    if weekday == 'M':
                        days.append(start)
                    if weekday == 'T':
                        days.append(start + 1)
                    if weekday == 'W':
                        days.append(start + 2)
                    if weekday == 'R':
                        days.append(start + 3)
                    if weekday == 'F':
                        days.append(start + 4)
                setattr(course, 'days', days)
                        
                        
            term['units'] = units
            totalUnits += units
        years[i]['terms'] = terms
            
    args['years'] = years
    args['totalUnits'] = totalUnits
    return render_to_response('planner/index.html', args, context_instance=RequestContext(request))