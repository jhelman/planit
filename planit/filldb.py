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
        c = course=Course.objects.filter(identifier=cname)
        if c:
            tm = TagMapping(tag=t, course=Course.objects.filter(identifier=cname)[0])
            tm.save()
    return t
    
def add_tags(arr):
    for cname in arr:
        tag = Tag(name=cname+"_tag")
        tag.save()
        c = course=Course.objects.filter(identifier=cname)
        if c:
            print cname
            tm = TagMapping(tag=tag,course=c[0])
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
     
                e=Enrollment(course=co, plan=p, units=co.course.max_units)
                e.save()
    
    arbrs = [ (RequirementGroup(major=m, name='MATH 41', n_prereqs=1), add_tag('Math_41', ['MATH41'])),
              (RequirementGroup(major=m, name='MATH 42', n_prereqs=1), add_tag('Math_42', ['MATH42'])),
              (RequirementGroup(major=m, name='CS 103', n_prereqs=1), add_tag('CS_103', ['CS103'])),
              (RequirementGroup(major=m, name='CS 109', n_prereqs=1), add_tag('CS_109', ['CS109']))]

    for rg, rtag in arbrs:
        rg.save()
        req = Requirement(name=rtag.name, fulfillers=rtag, n_class=1,  group=rg)
        req.save()
        
    electives = RequirementGroup(major=m, name='Math Electives', n_prereqs=1)
    electives.save()

    fiftiest = add_tag('MATH52_53', ['MATH52', 'MATH53'])
    fiftiesr = Requirement(name='MATH52/53', fulfillers=fiftiest, n_class=2, group=electives)
    fiftiesr.save()
    others = add_tag('MATH_elective', ['MATH51', 'MATH103', 'MATH104', 'MATH108', 'MATH109', 'MATH110', 'MATH113', 'CS157', 'CS205A'])
    req = Requirement(name="Math Electives", fulfillers=others, n_class=4,  group=electives)
    req.save()

    econ1a = Course.objects.filter(identifier__startswith="ECON1A")[0]
    econ1b = Course.objects.filter(identifier__startswith="ECON1B")[0]
    econ50 = Course.objects.filter(identifier__startswith="ECON50")[0]
    econ51 = Course.objects.filter(identifier__startswith="ECON51")[0]
    econ52 = Course.objects.filter(identifier__startswith="ECON52")[0]
    econ102a = Course.objects.filter(identifier__startswith="ECON102A")[0]
    econ102b = Course.objects.filter(identifier__startswith="ECON102B")[0]
    econ1bpg=PrereqGroup(for_course=econ1b, mandatory=True)
    econ1bpg.save()
    econ1bpg.satisfiers.add(econ1a)
    econ1bpg.save()
    econ50pg=PrereqGroup(for_course=econ50, mandatory=True)
    econ50pg.save()
    econ50pg.satisfiers.add(econ1a)
    econ50pg.save()
    econ51pg=PrereqGroup(for_course=econ51, mandatory=True)
    econ51pg.save()
    econ51pg.satisfiers.add(econ50)
    econ51pg.save()
    econ52pg=PrereqGroup(for_course=econ52, mandatory=True)
    econ52pg.save()
    econ52pg.satisfiers.add(econ1b)
    econ52pg.satisfiers.add(econ50)
    econ52pg.save()
    econ102apg=PrereqGroup(for_course=econ102a, mandatory=True)
    econ102apg.save()
    econ102apg.satisfiers.add(econ1a)
    econ102apg.save()
    econ102bpg=PrereqGroup(for_course=econ102b, mandatory=True)
    econ102bpg.save()
    econ102bpg.satisfiers.add(econ102a)
    econ102bpg.save()


    cs106a = Course.objects.filter(identifier__startswith="CS106A")[0]
    cs106b = Course.objects.filter(identifier__startswith="CS106B")[0]
    cs106bpg=PrereqGroup(for_course=cs106b, mandatory=False)
    cs106bpg.save()
    cs106bpg.satisfiers.add(cs106a)
    cs106bpg.save()

    cs110 = Course.objects.filter(identifier__startswith="CS110")[0]
    cs110pg=PrereqGroup(for_course=cs110, mandatory=False)
    cs110pg.save()
    cs110pg.satisfiers.add(cs106b)
    cs110pg.save()

    cs140 = Course.objects.filter(identifier__startswith="CS140")[0]
    cs140pg=PrereqGroup(for_course=cs140, mandatory=False)
    cs140pg.save()
    cs140pg.satisfiers.add(cs110)
    cs140pg.save()

    cs155 = Course.objects.filter(identifier__startswith="CS155")[0]
    cs155pg=PrereqGroup(for_course=cs155, mandatory=False)
    cs155pg.save()
    cs155pg.satisfiers.add(cs140)
    cs155pg.save()

 
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
