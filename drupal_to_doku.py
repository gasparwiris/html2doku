# -*- coding: utf-8 -*-

import lxml.html

inline_elements = {
        'b': ('**','**'),
        'i': ('//','//'),
        'em': ('//','//'),
        'strong': ('**','**'),
        'span': ('<no>SPAN</no>','<no>SPAN</no>'),
        'sub': ('<sub>','</sub>'),
        'sup': ('<sup>','</sup>'),
        'kbd': ('<key>','</key>'),
        'del': ('<del>','</del>'),
        'code': ('\'\'','\'\'')
        }
block_elements = {
        'p': ('',''),
        'h1': ('====== ',' ======'),
        'h2': ('===== ',' ====='),
        'h3': ('==== ',' ===='),
        'h4': ('== ',' =='),
        'h5': ('= ',' ='),
        }
void_elements = {
        'br':'\n\n',
        'hr':'\n----\n'
        }
special_elements = {
        'a',
        'pre',
        'img',
        'ol',
        'ul',
        'li',
        'table'
        }

class mutable_string:
    def __init__(self,**args):
        for (key, value) in args.items():
            setattr(self, key, value) #apparently this doesn't use unicode

def get_style(element,parent_style):
    tag = element.tag
    if parent_style == 'inline' and tag in block_elements:
        print('block inside inline!')
    if tag in inline_elements:
        return 'inline'
    if tag in block_elements:
        return 'block'
    if tag in void_elements:
        return 'void'
    if tag in special_elements:
        return 'special'
    else:
        return 'invalid'

# temporary

def process_special(element,main_text):
    main_text.s += '\n' + lxml.html.tostring(element) + '\n'
    return

def process_invalid(element,main_text):
    tag = element.tag
    if element.text != None:
        inner_text = element.text
    else:
        inner_text = ''
    main_text.s += '<%s>%s' % (tag, inner_text)
    children = list(element)
    for child in children:
        process_element(child,main_text,'invalid')
    if element.tail != None:
        tail_text = element.tail
    else:
        tail_text = ''
    main_text.s += '%s</%s>' % (tail_text, tag)
    return

def process_void(element,main_text):
    tag = element.tag
    if element.text != None:
        inner_text = element.text
    else:
        inner_text = ''
    main_text.s += void_elements[tag] + inner_text
    children = list(element)
    for child in children:
        process_element(child,main_text,'void')
    if element.tail != None:
        tail_text = element.tail
    else:
        tail_text = ''
    main_text.s += tail_text
    return

def process_inline(element,main_text):
    tag = element.tag
    if element.text != None:
        inner_text = element.text
    else:
        inner_text = ''
    print('inner: %s' % inner_text)
    main_text.s += inline_elements[tag][0] + inner_text
    children = list(element)
    for child in children:
        process_element(child,main_text,'inline')
    if element.tail != None:
        tail_text = element.tail
    else:
        tail_text = ''
    main_text.s += inline_elements[tag][1] + tail_text
    return

def process_block(element,main_text):
    if element.text != None:
        inner_text = element.text
    else:
        inner_text = ''
    main_text.s += '\n\n' + block_elements[element.tag][0] + inner_text
    children = list(element)
    for child in children:
        process_element(child,main_text,'block')
    if element.tail != None:
        tail_text = element.tail
    else:
        tail_text = ''
    main_text.s += block_elements[element.tag][1] + tail_text + '\n\n'
    return

def process_element(element,main_text,parent_style):
#    strip_tags(element,'div','center')
    style = get_style(element,parent_style)
    print('processing %s tag, type %s' % (element.tag, style))
    for child in list(element):
        print('has child %s' % child.tag)
    if style == 'inline':
        process_inline(element,main_text)
    elif style == 'block':
        process_block(element,main_text)
    elif style == 'void':
        process_void(element,main_text)
    elif style == 'special':
        process_special(element,main_text)
    else:
        process_invalid(element,main_text)
    return

doc = lxml.html.parse('test.html')
result  = mutable_string(s=u'')
process_element(doc.getroot(),result,'block')
out = open('test.txt','w')
out.write(result.s.encode('utf-8'))
out.close()



