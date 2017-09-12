# -*- coding: utf-8 -*-

import lxml.etree
from html_to_doku import Html_pre

class mutable_string:
    def __init__(self,**args):
        for (key, value) in args.items():
            setattr(self, key, value) #apparently this doesn't use unicode

def process_element(element,main_text):
    current = Html_pre(element)
    main_text.s += current.print_head()
    for child in list(element):
        process_element(child,main_text)
    main_text.s += current.print_tail()


parser = lxml.etree.HTMLParser(remove_comments=True)
doc = lxml.etree.parse('test.html',parser)
lxml.etree.strip_tags(doc.getroot(),
                 'html',
                 'head',
                 'body',
                 'meta',
                 'link',
                 'script',
                 'style',
                 'div',
                 'center')
result  = mutable_string(s=u'')
process_element(doc.getroot(),result)
out = open('test.txt','w')
out.write(result.s.encode('utf-8'))
out.close()



