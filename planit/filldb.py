from xml.etree.ElementTree import ElementTree
from collections import deque
from string import whitespace
from time import strptime
import os
import random
from datetime import datetime
try:
    from planner.models import *
except Exception:
    pass

def catch_save(obj):
    try:
        obj.save()
    except Exception:
        return

def term_num_for_str(nstr):
    term_num = -1
    if nstr == 'autumn':
        term_num = 0
    elif nstr == 'winter':
        term_num = 1
    elif nstr == 'spring':
        term_num = 2
    elif nstr == 'summer':
        term_num = 3
    return term_num

def parse_section(section, course, year):
    i = section.find('instructor')
    ins = None
    if i is not None:
        fn = i.find('firstName').text
        ln = i.find('lastName').text
        ins = Instructor.objects.filter(first_name=fn, last_name=ln)
        if not ins:
            ins = Instructor(first_name=fn, last_name=ln)
            ins.save()
        else:
            ins = ins[0]
            
    sch = section.find('schedules')
    term = term_num_for_str(section.find('term').text.split(' ')[-1].lower())

    t = Term.objects.filter(num=term)
    if not t:
        t = Term(num=term)
        catch_save(t)
    else:
        t=t[0]
    for schedule in sch.getiterator(tag='schedule'):
        start_t = schedule.find('startTime').text
        end_t =  schedule.find('endTime').text
        start_t = datetime.datetime(*strptime(start_t, "%I:%M:%S %p")[0:6]).time()
        end_t = datetime.datetime(*strptime(end_t, "%I:%M:%S %p")[0:6]).time()
        days_list = schedule.find('days').text.split()
        daystr = "".join([word[0] if word[0:2] != 'Th' else 'R' for word in days_list])
        for year in range(4):
            co = CourseOffering.objects.filter(course=course, year=(2008 + year), term=t, 
                start_time=start_t, end_time=end_t, weekdays=daystr, instructor=ins)
            if not co:
                co = CourseOffering(course=course, year=(2008+year), term=t, start_time=start_t, 
                        end_time=end_t, weekdays=daystr, instructor=ins)
                catch_save(co)

def make_tags(tag_strs, course):
    for tag in tag_strs:
        indb = Tag.objects.filter(name=tag)
        if not indb:
            indb = Tag(name=tag)
            catch_save(indb)
        else:
            indb = indb[0]

        tm = TagMapping(tag=indb, course=course)
        tm.save()

def parse_course(course_elem):
    idstr = course_elem.find('subject').text + course_elem.find('code').text
    idnum = int(course_elem.find('administrativeInformation').find('courseId').text)
    title = course_elem.find('title').text
    year = 2008 + random.randint(0, 4)  #int(course_elem.find('year').text.split('-')[1])
    desc = course_elem.find('description').text
    if(desc is None):
        desc = ""
    max_u = int(course_elem.find('unitsMax').text)
    min_u = int(course_elem.find('unitsMin').text)
    c = Course.objects.filter(identifier=idstr, title=title, description=desc, class_number=idnum,
        max_units=max_u, min_units=min_u)
    if not c:
        c = Course(identifier=idstr, title=title, description=desc, class_number=idnum,
            max_units=max_u, min_units=min_u)
        catch_save(c)
    else:
        c = c[0]

    tags = course_elem.find('gers').text
    if tags:
        tagl = tags.split(', ')
        make_tags(tagl, c)
    
    s = course_elem.find('sections')
    for section in s.getiterator(tag='section'):
        sec_type = section.find('component').text
        if (sec_type == "DIS" or sec_type == "INS" or sec_type == "T/D"):
            continue
        parse_section(section, c, year)

def parse_document(fname):
    e = ElementTree()
    e.parse(fname)
    root = e.getroot()
    for elem in e.getiterator(tag='course'):
        parse_course(elem)

def add_req(name, tag, courses, n, type_):
    t=Tag(name=tag)
    t.save()
    for course in courses:
        tm = TagMapping(tag=t, course=Course.objects.filter(identifier=course)[0])
        tm.save()

    #rg = Requirem
    #r = Requirement(name=name, fulfillers=t, n_class=n, force=False, 
    return r

def add_tag(tag_str, arr):
    t=Tag(name=tag_str)
    t.save()
    for cname in arr:
        tm = TagMapping(tag=t, course=Course.objects.filter(identifier=cname)[0])
        tm.save()
    return t
    
def add_tags(arr):
    for cname in arr:
        tag = Tag(name=cname+"_tag")
        tag.save()
        tm = TagMapping(tag=tag, course=Course.objects.filter(identifier=cname)[0])
        tm.save()

def filldb():
    for i in range(3):
        t=Term(i)
        t.save()
    fnames = ['cs.xml', 'math.xml', 'ihum.xml', 'physics.xml', 'humbio.xml', 'econ.xml', 'me.xml']
    for fname in fnames:
        parse_document(fname)
    u=University(name='Stanford',max_units_per_quarter=20)
    u.save()
    m=Major(name='CS')
    m.save()
    p=Plan(student_name='Dan Vinegrad', university=u,
        major=m,start_year=2008,num_years=4)
    prefixes=['EC', 'HUM','ME'] 
    p.save()
    for y in range(4):
        for t in range(3):
            tn=Term(num=t)
            print t, " ", y
            co=CourseOffering.objects.filter(year=(2008 + y), term__num=t, course__identifier__startswith=prefixes[t])
            if co:
                co=co[random.randint(0, len(co) - 1)]
     
                e=Enrollment(course=co, plan=p)
                e.save()

    rg = RequirementGroup(major=m, name='math', n_prereqs=7)
    rg.save()

    basic_math = Tag(name='basic math')
    basic_math.save()
    maths = add_tag('basic_math', ['MATH41', 'MATH42', 'CS103', 'CS109'])
    fifties = add_tag('fifties', ['MATH52', 'MATH53'])

    basic_math = Requirement(name='basic_math', fulfillers=maths, n_class=4, 
        force=False, group=rg)

    basic_math = Requirement(name='advanced fifties', fulfillers=fifties, n_class=2, 
        force=False, group=rg)

    basic_math.save()
    fifties.save()

    others = ['MATH51', 'MATH103', 'MATH104', 'MATH108', 'MATH109', 
        'MATH110', 'MATH113', 'CS157, CS205A'] 

    for o in others:
        selftag = Tag(name=o+"_tag")
        selftag.save()
        req = Requirement(name=o + "_req", fulfillers=selftag, 
            n_class=1, force=False, group=rg)
        req.save()
    
    #scr = add_req('Science', 'sci', ['PHYSICS41', 'PHYSICS43'])
    #ef = add_req('Engineering Fundamentals', 'engr', ['CS106B', 'ENGR40'])
    #csc = add_req('CS Core', 'cs_core', ['CS107', 'CS110', 'CS161'])
    #sd = add_req('Systems Depth', 'cs_sys_depth', ['CS140', 'CS143'])

def main():
    print "Wrong wrong wrong (not that there's anyway you'd know that...)"
    print "to fill the database:"
    print "$: python manage.py shell"
    print ">>> import filldb"
    print ">>> filldb.filldb()"
    
if __name__ == '__main__':
    main()
