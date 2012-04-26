from mako.template import Template
from xml.etree.ElementTree import ElementTree
from collections import deque

def parse_requirement(node):
    fields = {}
    for child in node:
        for key in child.keys():
            if key =='li':
                opt_str = child.attrib.get(key)
                opts = [opt.strip() for opt in opt_str.split()]
                fields[child.tag] = opts
            else:
                fields[child.tag] = child.attrib.get(key)
    return fields

def bfs(start):
    reqs = []
    s = deque()
    s.append(start)
    while(len(s) != 0):
        cur = s.popleft()
        for child in list(cur):
            fields = parse_requirement(child)
            reqs.append((child.tag, fields))
            
    return reqs

def main():
    
    e = ElementTree()
    e.parse('in.xml')
    reqlist = bfs(e.getroot())

    my = Template(filename='out.tmp')
    outpy = open('models.py', 'w+')    
    outpy.write(my.render(var_name='"hello, world"', reqs=reqlist))

if __name__=='__main__':
    main()
