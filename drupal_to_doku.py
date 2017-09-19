# -*- coding: utf-8 -*-

import lxml.etree
import io
import sys
from html_to_doku import Html_pre

def process_element(htmlnode,main_text):
    current = htmlnode
    main_text.write(current.print_head())
    currentinfo = current.getinfo()
    for child in list(current.element):
        next = Html_pre(child,currentinfo)
        process_element(next,main_text)
    main_text.write(current.print_tail())

def remove_tags(document,*tags):
    for tag in tags:
        for element in document.findall('.//'+tag):
            document.remove(element)

parser = lxml.etree.HTMLParser(remove_comments=True)

#temporary, for testing

if len(sys.argv):
    test = sys.argv[1]
else:
    test = 'test.html'

doc = lxml.etree.parse(test,parser).getroot()
remove_tags(doc,'head','link','meta','style','script')
root = Html_pre(doc)
lxml.etree.strip_tags(root.element,'body','center','blockquote')


result = io.StringIO(u'')
process_element(root,result)
out = open('/home/gaspar/host/test.txt','wb+')
out.write(result.getvalue().encode('utf-8'))
out.close()
