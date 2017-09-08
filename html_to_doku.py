# -*- coding: utf-8 -*-

def _empty_if_none(text):
    if text == None:
        return ''
    else:
        return text

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
            'code': ('\'\'','\'\'')
            },
        'block': {
            'p': ('',''),
            'h1': ('====== ',' ======'),
            'h2': ('===== ',' ====='),
            'h3': ('==== ',' ===='),
            'h4': ('== ',' =='),
            'h5': ('= ',' ='),
            },
        'void': {
            'br':('\n\n',''),
            'hr':('\n----\n','')
            },
        'special': {
            'a',
            #'pre',
            #'img',
            #'ol',
            #'ul',
            #'li',
            #'table'
            }
        }

class Html_pre:
    def __print_special_head(self):
        if self.element.tag == 'a':
            return self.__print_anchor_h()
            #'pre': self.__print_pre_h,
            #'img': self.__print_img_h,
            #'ol': self.__print_ol_h,
            #'ul': self.__print_ul_h,
            #'li': self.__print_li_h,
            #'table': self.__print_table_h

    def __print_special_tail(self):
        if self.element.tag == 'a':
            return self.__print_anchor_t()
            #'pre': self.__print_pre_t,
            #'img': self.__print_img_t,
            #'ol': self.__print_ol_t,
            #'ul': self.__print_ul_t,
            #'li': self.__print_li_t,
            #'table': self.__print_table_t

    #TODO: handle a tags that are only anchors
    def __print_anchor_h(self):
        if 'href' not in self.element.attrib:
            self.style = 'invalid'
            return self.print_head()
        return ('[[' + _empty_if_none(self.element.attrib['href'])
                +'|') 

    def __print_anchor_t(self):
        if 'href' not in self.element.attrib:
            self.style = 'invalid'
            return self.print_tail()
        return ']]'
        

    def __get_style(self):
        for _style in _styles:
            if self.element.tag in _styles[_style]:
                self.style = _style
                return
        self.style = 'invalid'
    
    def print_head(self):
        if self.style == 'invalid':
            return '<%s>%s' % (self.element.tag,
                               _empty_if_none(self.element.text))
        if self.style == 'special':
            return (self.__print_special_head()
                    + _empty_if_none(self.element.text))
        return (_styles[self.style][self.element.tag][0]
                + _empty_if_none(self.element.text))
    
    def print_tail(self):
        if self.style == 'invalid':
            return '</%s>%s' % (self.element.tag,
                                _empty_if_none(self.element.tail))
        if self.style == 'special':
            return (self.__print_special_tail()
                    + _empty_if_none(self.element.tail))
        return (_styles[self.style][self.element.tag][1]
                + _empty_if_none(self.element.tail))

    def __init__(self,init_element):
        self.element = init_element
        self.__get_style()
