# -*- coding: utf-8 -*-

from lxml import HtmlElement

class Html_pre(HtmlElement):
    __styles = {
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
                }
            'block': {
                'p': ('',''),
                'h1': ('====== ',' ======'),
                'h2': ('===== ',' ====='),
                'h3': ('==== ',' ===='),
                'h4': ('== ',' =='),
                'h5': ('= ',' ='),
                }
            'void': {
                'br':('\n\n',''),
                'hr':('\n----\n','')
                }
            'special': {
                'a',
                'pre',
                'img',
                'ol',
                'ul',
                'li',
                'table'
                }
            }
    __print_special_head = {
            'a': self.__print_anchor_h,
            'pre': self.__print_pre_h,
            'img': self.__print_img_h,
            'ol': self.__print_ol_h,
            'ul': self.__print_ul_h,
            'li': self.__print_li_h,
            'table': self.__print_table_h
            }
    __print_special_tail = {
            'a': self.__print_a_t,
            'pre': self.__print_pre_t,
            'img': self.__print_img_t,
            'ol': self.__print_ol_t,
            'ul': self.__print_ul_t,
            'li': self.__print_li_t,
            'table': self.__print_table_t
            }
    def __print_anchor_h(self):
        return '[['+self.attrib['href']+'|'
        
    def __empty_if_none(text):
        if text == None:
            return ''
        else:
            return text

    def __get_style(self):
        for _style in self.__styles:
            if self.tag in self.__styles[_style]:
                self.style = _style
                return
        self.style = 'invalid'
    
    def print_head(self):
        if self.style == 'invalid':
            return '<%s>%s' % (self.tag, __empty_if_none(self.text))
        if self.style == 'special':
            return (self.__print_special_head[self.tag]()
                    + __empty_if_none(self.text))
        return (self.__styles[self.style][self.tag][0]
                + self.__empty_if_none(self.text))
    
    def print_tail(self):
        if self.style == 'invalid':
            return '</%s>%s' % (self.tag, __empty_if_none(self.tail))
        if self.style == 'special':
            return (self.__print_special_tail[self.tag]()
                    + __empty_if_none(self.tail))
        return (self.__styles[self.style][self.tag][1]
                + self.__empty_if_none(self.tail))

    def __init__(self):
        HtmlElement.__init__(self)
        self.__get_style()
