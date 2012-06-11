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
                reqs.append(req.upper())
        else:
            for m in re.finditer('(?P<num>\d{1,3}[A-Z]?)', pat_str):
                req = dept + m.group('num') 
                req = 'CS106B'if req == 'CS106' else req
                reqs.append(req.upper())
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
    rg = RequirementGroup(major=m, name=rg_name, n_reqs=n)
    rg.save()

    tags = None
    r_n = 1
    r_name = ""
    classes = set(classes)
    for c in classes:
        if c.find(",") != -1:
            c = c.split(',')
            r_n = int(c.pop())        
            r_name = "+".join(c)
        else:
            r_name = c
            c = [c]
            
        tag = add_tag(r_name, c)
        req = Requirement(name=tag.name, fulfillers=tag, n_class=r_n, group=rg, exclusive=exclusive)
        req.save()
    return rg

def filldb():
    for i in range(3):
        t=Term(i)
        t.save()
    fnames = ['all2.xml']#'cs.xml', 'math.xml', 'ihum.xml', 'physics.xml', 'humbio.xml', 'econ.xml', 'me.xml', 'engr.xml']
    for fname in fnames:
        parse_document(fname)
    u=University(name='Stanford',max_units_per_quarter=20)
    u.save()
    m=Major(name='ECON')
    m.save()
    m=Major(name='CS')
    m.save()
    user = User.objects.create_user('dv', 'dv@dv.dv', 'dv')
    user.first_name='Dan'
    user.last_name='Vinegrad'
    user.save()
    
    for cname, pl in prereqs.iteritems():
        try:
            c = course=Course.objects.get(identifier=cname)
            for p in pl:
                pg=PrereqGroup(for_course=c, mandatory=cname.startswith('ECON'))
                pg.save()
                pc = Course.objects.get(identifier=p)
                pg.satisfiers.add(pc)
                pg.save()
        except Exception:
            pass
	
    majors = json.loads(open("majors.json").read())
    for major, rgs in majors.iteritems():
        major_obj = Major.objects.get(name=major)
        for rg_name, rg_dict in rgs.iteritems():
            if rg_name == u"tracks":
                for trackname, trackdata in rg_dict.iteritems():
                    make_rg(major_obj, major + " " + trackname, trackdata, True, True)
                continue
            add_requirement_group(major_obj, major + " " + rg_name, rg_dict["n"], rg_dict["classes"])
            #rg = RequirementGroup(

    ecs = Tag.objects.filter(name__startswith='GER:EC')
    ecrg = RequirementGroup(major=None, name="GER:EC", n_reqs=2)  
    ecrg.save()
    for ec in ecs:
        r = Requirement(name=ec.name, fulfillers=ec, n_class=1, group=ecrg, bypassable=False)
        r.save()

    other_gers = (set(Tag.objects.filter(name__startswith='GER:')) | set(Tag.objects.filter(name__startswith='Writing'))) - set(ecs)
    for ger in other_gers:
        if ger.name=='WritingSLE':
            continue
        gerg = RequirementGroup(major=None, name=ger.name, n_reqs=1)  
        gerg.save()
        r = Requirement(name=ger.name, fulfillers=ger, n_class=1, group=gerg, bypassable=False)
        r.save()

def make_rg(m, name, rgdata, track, exclusive=False):
    rg = RequirementGroup(major=m, name=name, n_reqs=rgdata["n"])
    rg.save()
    del rgdata["n"]
    for reqname, reqdata in rgdata.iteritems():
        classes = set(reqdata["classes"])
        tag = add_tag(reqname, classes)
        req = Requirement(name=name + " " + tag.name, fulfillers=tag, n_class=reqdata["n"], group=rg, exclusive=exclusive)
        req.save()
        rg.save()

    m.tracks.add(rg)
    m.save()
    rg.is_track=track
    rg.save()
    return rg

def main():
    print "to fill the database:"
    print "$: python manage.py shell"
    print ">>> import filldb"
    print ">>> filldb.filldb()"
    
if __name__ == '__main__':
    main()
