from xml.etree.ElementTree import ElementTree
from collections import deque
from string import whitespace
from time import strptime
import os
import random
from datetime import datetime
import re
import sys
import collections
import json

try:
    from planner.models import *
except Exception:
    pass

def catch_save(obj):
    try:
        obj.save()
    except Exception:
        return

prereqs = collections.defaultdict(dict)

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
        try:
            start_t = datetime.datetime(*strptime(start_t, "%I:%M:%S %p")[0:6]).time()
            end_t = datetime.datetime(*strptime(end_t, "%I:%M:%S %p")[0:6]).time()
        except Exception:
            start_t = datetime.datetime(*strptime(start_t, "%H:%M:%S")[0:6]).time()
            end_t = datetime.datetime(*strptime(end_t, "%H:%M:%S")[0:6]).time()

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

def find_prereqs(desc, dept):
    pat_match = re.search("[pP]rerequisites?:?\s*(?P<content>.*)", desc, re.UNICODE)
    reqs = []
    if pat_match is not None:
        pat_str = pat_match.group('content')
        if( pat_str.find("or") != -1):
            pat_str = pat_str[:pat_str.find("or")]

        ms = [s for s in re.finditer("(?P<dept>[A-Z]{2,})\s*(?P<num>\d{1,3}[A-Z]?)", pat_str)]
        if ms:
            for m in ms:
                req = m.group('dept') + m.group('num') 
                req = 'CS106B'if req == 'CS106' else req
                reqs.append(req)
        else:
            for m in re.finditer('(?P<num>\d{1,3}[A-Z]?)', pat_str):
                req = dept + m.group('num') 
                req = 'CS106B'if req == 'CS106' else req
                reqs.append(req)
    return reqs

def parse_course(course_elem):
    dept = course_elem.find('subject').text
    code = course_elem.find('code').text
    idstr = dept + code
    #print idstr
    int_code = filter(lambda x: x.isdigit(), code) # for courses like MATH51H, CS106A, etc, just want the int part
    if int_code == '':
        return
    int_code = int(int_code)
    idnum = int(course_elem.find('administrativeInformation').find('courseId').text)
    title = course_elem.find('title').text
    year = 2008 + random.randint(0, 4)  #int(course_elem.find('year').text.split('-')[1])
    desc = course_elem.find('description').text
    if(desc is None):
        desc = ""
    course_prereqs = find_prereqs(desc, dept)
    if course_prereqs:
        prereqs[idstr] = course_prereqs
    max_u = int(course_elem.find('unitsMax').text)
    min_u = int(course_elem.find('unitsMin').text)
    c = Course.objects.filter(identifier=idstr, dept=dept, code=int_code, title=title, description=desc, class_number=idnum,
        max_units=max_u, min_units=min_u)
    if not c:
        c = Course(identifier=idstr, dept=dept, code=int_code, title=title, description=desc, class_number=idnum,
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
            tm = TagMapping(tag=t, course=Course.objects.filter(identifier__startswith=cname)[0])
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
def add_requirement_group(m, rg_name, n, classes, exclusive=False):
    rg = RequirementGroup(major=m, name=rg_name, n_prereqs=n)
    rg.save()

    tags = [add_tag(c, [c]) for c in classes]
    reqs = [Requirement(name=t.name, fulfillers=t,n_class=1, group=rg, exclusive=exclusive) for t in tags]
    for r in reqs:
        r.save()
    return rg

def filldb():
    for i in range(3):
        t=Term(i)
        t.save()
    fnames = ['cs.xml', 'math.xml', 'ihum.xml', 'physics.xml', 'humbio.xml', 'econ.xml', 'me.xml', 'engr.xml']
    for fname in fnames:
        parse_document(fname)
    u=University(name='Stanford',max_units_per_quarter=20)
    u.save()
    m=Major(name='CS')
    m.save()
    user = User.objects.create_user('dv', 'dv@dv.dv', 'dv')
    user.first_name='Dan'
    user.last_name='Vinegrad'
    user.save()
    p=Plan(user=user, name='Dan Vinegrad', university=u,
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
    print prereqs['ECON50']
    for cname, pl in prereqs.iteritems():
        try:
            c = course=Course.objects.get(identifier=cname)
            pg=PrereqGroup(for_course=c, mandatory=cname.startswith('ECON'))
            pg.save()
            for p in pl:
                pc = Course.objects.get(identifier=p)
                pg.satisfiers.add(pc)
                pg.save()
        except Exception:
            pass

    json.loads(open("cs_major.json").read())
"""    
    math_corerg = add_requirement_group(m, "Math Core", 4, ["MATH41", "MATH42", "CS103", "CS109"]) 
    math_electives = ['MATH51', 'MATH104','MATH108','MATH109','MATH110','MATH113','CS157','CS205A']
    math_electives = add_requirement_group(m, "Math Electives", 2, math_electives) 

    fiftiest = add_tag('MATH52_53', ['MATH52', 'MATH53'])
    fiftiesr = Requirement(name='MATH52+53', fulfillers=fiftiest, n_class=2, group=math_electives)
    fiftiesr.save()
########################
    sci_corerg = add_requirement_group(m, "Science Core", 2, ['PHYSICS41','PHYSICS43']) 
    sci_electives = ['BIO41', 'BIO42', 'BIO43', 'CEE63', 'CEE64', 'CEE70', 'CHEM31A', 'CHEM31B', 'CHEM33', 'CHEM35',
                     'CHEM36', 'CHEM131', 'CHEM135', 'EARTHSYS10', 'ENGR31', 'GES1A', 'GES1B', 'GES1C', 'PHYSICS21',
                     'PHYSICS23', 'PHYSICS25', 'PHYSICS45', 'PHYSICS61', 'PHYSICS63', 'PHYSICS65']
    sci_electives = add_requirement_group(m, "Science Electives", 1, sci_electives) 
########################
    win_corerg = add_requirement_group(m, "Writing in the Major", 1, ['CS191W','CS194W', 'CS210B', 'CS294W', 'CS181W']) 
########################
    tis_corerg = add_requirement_group(m, "Technology in Society", 1, ['STS101','STS112', 'STS115', 'BIOE131', 'CS181', 'CS181W', 'ENGR145', 'HUMBIO174', 'MSE181', 'MSE193', 'POLISCI114S', 'PUBLPOL194']) 
######################
    ef_core = add_requirement_group(m, "Engineering Fundamentals", 2, ["ENGR40"], True) 

    cs_intro = add_tag('CS106', ['CS106B', 'CS106X'])
    cs_intro = Requirement(name='CS106', fulfillers=cs_intro, n_class=1, group=ef_core, exclusive=True)
    cs_intro.save()

    ef_electives = ['ENGR10', 'ENGR14','ENGR15', 'ENGR20','ENGR25B','ENGR25E','ENGR30','ENGR40','ENGR40N','ENGR40P',
                    'ENGR50','ENGR50E','ENGR50M','ENGR60','ENGR62','ENGR80', 'ENGR90']
    ef_electives = add_requirement_group(m, "Engineering Electives", 1, ef_electives, True) 
##########################
    cs_core = add_requirement_group(m, "CS Core", 3, ["CS107", "CS110", "CS161"], True) 
##########################

##########################
##########################

    sys_core = add_requirement_group(m, "Track Depth (Systems)", 4, ["CS140"], True) 
    sys_core.is_track=True
    sys_core.save()
    sys_ass = add_tag('EE108B/CS143', ['EE108B', 'CS143'])
    sys_ass = Requirement(name='Track Requirements (Systems)', fulfillers=sys_ass, n_class=1, group=sys_core, exclusive=True)
    sys_ass.save()
    
    track_electives = add_tag('Track Electives (Systems)', ['CS144', 'CS145', 'CS149', 'CS155', 'CS240', 'CS242', 'CS243', 'CS244', 'CS245', 'EE271', 'CS282'])		
    track_electives = Requirement(name='Track Electives', fulfillers=track_electives, n_class=2, group=sys_core, exclusive=True)
    track_electives.save()
		
    gen_elecs = ['CS240E', 'CS244C', 'CS244E', 'CS315A', 'CS315B', 'CS341', 'CS343', 'CS344', 'CS344E', 'CS345', 'CS346', 'CS347', 
								 'CS448', 'EE382A', 'EE382C', 'EE384A', 'EE384B', 'EE384C', 'EE384S', 'EE384X', 'EE384Y', 'CS108', 'CS121'  'CS221', 'CS124', 
								 'CS142', 'CS143', 'CS144', 'CS145', 'CS147', 'CS148', 'CS149', 'CS154', 'CS155', 'CS156', 'CS157', 'CS151', 'CS164', 'CS205A', 
								 'CS205B', 'CS210A', 'CS222', 'CS223A', 'CS223B', 'CS224M', 'CS24N', 'CS224S', 'CS224U', 'CS224W', 'CS225A', 'CS225B', 'CS226', 
								 'CS227', 'CS228', 'CS228T', 'CS229', 'CS240', 'CS241', 'CS242', 'CS243', 'CS244', 'CS244B', 'CS245', 'CS246', 'CS247', 'CS248', 
								 'CS249A', 'CS249B', 'CS254', 'CS255', 'CS256', 'CS257', 'CS258', 'CS261', 'CS262', 'CS270', 'CS271', 'CS272', 'CS273A', 'CS274', 
								 'CS276', 'CS277', 'CS295', 'CME108', 'EE108B', 'CS282']
    gen_elecs = add_tag('General Electives', gen_elecs)
    gen_elecs = Requirement(name='General Electives', fulfillers=gen_elecs, n_class=3, group=sys_core, exclusive=True)
    gen_elecs.save()

    m.tracks.add(sys_core)		
    m.save()


    p.track = sys_core
    p.save()
    ecs = Tag.objects.filter(name__startswith='GER:EC')
    ecrg = RequirementGroup(major=None, name="GER:EC", n_prereqs=2)  
    ecrg.save()
    for ec in ecs:
        r = Requirement(name=ec.name, fulfillers=ec, n_class=1, group=ecrg, bypassable=False)
        r.save()

    other_gers = (set(Tag.objects.filter(name__startswith='GER:')) | set(Tag.objects.filter(name__startswith='Writing'))) - set(ecs)
    for ger in other_gers:
        gerg = RequirementGroup(major=None, name=ger.name, n_prereqs=1)  
        gerg.save()
        r = Requirement(name=ger.name, fulfillers=ger, n_class=1, group=gerg, bypassable=False)
        r.save()"""


def main():
    print "Wrong wrong wrong (not that there's anyway you'd know that...)"
    print "to fill the database:"
    print "$: python manage.py shell"
    print ">>> import filldb"
    print ">>> filldb.filldb()"
    
if __name__ == '__main__':
    main()
