# -*- coding: utf-8 -*-

import io

def _empty_if_none(text):
    if text == None or text.isspace():
        return ''
    else:
        return text

#TODO: figure out if constants go inside our outside class
_styles = {
        'inline': {
            'b': ('**','**'),
            'i': ('//','//'),
            'em': ('//','//'),
            'strong': ('**','**'),
            'span': ('<no>SPAN</no>','<no>SPAN</no>'),
            'sub': ('<sub>','</sub>'),
            'sup': ('<sup>','</sup>'),
            'kbd': ('<key>','</key>'),
            'del': ('<del>','</del>'),
            'code': ('\'\'','\'\''),
            'pre': ('<code>','</code>')
            },
        'block': {
            'html': ('',''),
            'center': ('','\n\n'),
            'div': ('','\n\n'),
            'p': ('','\n\n'),
            'h1': ('====== ',' ======\n\n'),
            'h2': ('===== ',' =====\n\n'),
            'h3': ('==== ',' ====\n\n'),
            'h4': ('== ',' ==\n\n'),
            'h5': ('= ',' =\n\n'),
            },
        'void': {
            'br':('','\n\n'),
            'hr':('----','\n\n')
            },
        'special': {
            'a',
            'img',
            'ol',
            'ul',
            'li',
            #'table',
            #'th',
            #'td'
            }
        }

_nestables = {'blockquote','ul','li'}

_default_parent = {
        'nestlevel': 0,
        'listtype': ''
        }

class Html_pre:
    def __print_special_head(self):
        if self.element.tag == 'a':
            return self.__print_anchor_h()
        elif self.element.tag == 'img':
            return self.__print_img_h()
        elif self.element.tag in ['ul','ol']:
            return self.__print_list_h()
        elif self.element.tag == 'li':
            return self.__print_li_h()
            #'table': self.__print_table_h

    def __print_special_tail(self):
        if self.element.tag == 'a':
            return self.__print_anchor_t()
        elif self.element.tag == 'img':
            return self.__print_img_t()
        elif self.element.tag in ['ul','ol']:
            return self.__print_list_h()
        elif self.element.tag == 'li':
            return self.__print_li_h()
            #'table': self.__print_table_t

    #TODO: handle a tags that are only anchors
    def __print_anchor_h(self):
        if 'href' not in self.element.attrib:
            self.style = 'invalid'
            return self.print_head()
        return ('[[' + _empty_if_none(self.element.attrib['href'])
                +'|'
                + _empty_if_none(self.element.text))

    def __print_anchor_t(self):
        if 'href' not in self.element.attrib:
            self.style = 'invalid'
            return self.print_tail()
        return ']]' + _empty_if_none(self.element.tail)

    def __print_img_h(self):
        if 'src' not in self.element.attrib:
            self.style = 'invalid'
            return self.print_head()
        return ('{{' + _empty_if_none(self.element.attrib['src']
                +'|')
                + _empty_if_none(self.element.text))

    def __print_img_t(self):
        if 'src' not in self.element.attrib:
            self.style = 'invalid'
            return self.print_tail()
        return '}}' + _empty_if_none(self.element.tail)

    def __print_list_h(self):
        self.listtype = self.element.tag
        return ''
    
    def __print_list_t(self):
        if self.nestlvl == 1:
            return '\n\n'
        else:
            return ''
    def __print_li_h(self):
        return (' ' * 2 * self.nestlevel) + '*'

    def __print_li_t(self):
        return '\n'

    def __get_style(self):
        for _style in _styles:
            if self.element.tag in _styles[_style]:
                self.style = _style
                return
        self.style = 'invalid'

    def getinfo(self):
        info = {}
        if self.element.tag == 'ol':
            info['listtype'] = 'ordered'
        elif self.element.tag == 'ul':
            info['listtype'] = 'unordered'
        else:
            info['listtype']=''
        info['nestlevel'] = self.nestlevel
        return info
    
    def print_head(self):
        if self.style == 'invalid':
            retval = '<%s>%s' % (self.element.tag,
                               _empty_if_none(self.element.text))
        elif self.style == 'special':
            retval =  self.__print_special_head()
        else:
            retval = (_styles[self.style][self.element.tag][0]
                      + _empty_if_none(self.element.text))
        return(unicode(retval))
    
    def print_tail(self):
        if self.style == 'invalid':
            retval =  '</%s>%s' % (self.element.tag,
                                _empty_if_none(self.element.tail))
        elif self.style == 'special':
            retval =  self.__print_special_tail()
        else:
            retval = (_styles[self.style][self.element.tag][1]
                      + _empty_if_none(self.element.tail))
        return unicode(retval)

    def __init__(self,init_element,parentinfo=_default_parent):
        print(init_element.tag)
        print(parentinfo)
        self.element = init_element
        self.nestlevel = parentinfo['nestlevel'] + 1
        self.listtype = parentinfo['listtype']
        self.__get_style()
