# -*- coding: utf-8 -*-

import lxml.etree
import io
import os
import sys
import configargparse
from html_to_doku import Html_pre

def process_element(htmlnode,main_text):
    current = htmlnode
    main_text.write(current.print_head())
    currentinfo = current.getinfo()
    for child in list(current.element):
        next = Html_pre(child,currentinfo)
        process_element(next,main_text)
    main_text.write(current.print_tail())

def strip_ids(document,idname):
    pass

exists_conf_file = False
HOMEDIR = os.path.expanduser('~')
CURRDIR = os.getcwd()
if os.path.isfile(os.path.join(CURRDIR,'h2dok.conf')):
    default_conf_file = os.path.join(CURRDIR,'h2dok.conf')
    exists_conf_file = True
elif os.path.isfile(os.path.join(HOMEDIR,'.h2dok')):
    default_conf_file = os.path.join(HOMEDIR,'.h2dok')
    exists_conf_file = True

argp = configargparse.ArgParser()
if exists_conf_file:
    argp.add('-c',
             '--config',
             nargs = '?',
             default = default_conf_file,
             type = str,
             metavar = 'Configuration file',
             is_config_file = True,
             help = ('Use the configuration file at the specified '
                     'path. If none specified, a default configuration '
                      'file is used.'))
else:
    argp.add('-c',
             '--config',
             nargs = '?',
             type = str,
             metavar = 'Configuration file',
             is_config_file = True,
             help = ('Use the configuration file at the specified '
                     'path. If none specified, a default configuration '
                      'file is used.'))

argp.add('--strip-tags',
         nargs = '+',
         metavar = 'TAGS',
         help = ('List of tags to strip from input. '
                 'Child tags of stripped tags are still '
                 'processed.'))
argp.add('--strip_ids',
         nargs = '+',
         metavar = 'IDS',
         help = ('List of id attribute values. Tags with '
                 'the specified values will be stripped '
                 'from input. Child tags of stripped tags '
                 'are still processed.'))
argp.add('--strip_classes',
         nargs = '+',
         metavar = 'CLASSES',
         help = ('List of class attribute values. Tags with '
                 'the specified values will be stripped '
                 'from input. Child tags of stripped tags '
                 'are still processed.'))
argp.add('--ignore-tags',
         nargs = '+',
         metavar = 'TAGS',
         help = ('List of tags to ignore from input. '
                 'Child tags of ignored tags are also '
                 'ignored.'))
argp.add('--ignore-ids',
         nargs = '+',
         metavar = 'IDS',
         help = ('List of id attribute values. '
                 'Tags with the specified values '
                 'will be ignored from input. Child tags '
                 'of ignored tags are also ignored.'))
argp.add('--ignore-classes',
         nargs = '+',
         metavar = 'CLASSES',
         help = ('List of class attribute values. '
                 'Tags with the specified values '
                 'will be ignored from input. Child tags '
                 'of ignored tags are also ignored.'))
argp.add('FILES',
         nargs = '+',
         help = ('List of relative or absolute paths to files or '
                 'directories passed to html2doku. If a directory '
                 'is given, html2doku will run on all \'.htm[l]\' '
                 'files in the directory.'))

args = argp.parse_args()

to_strip = []
for triple in zip(args.strip-tags,
                  args.strip-ids,
                  args.strip-classes):
    to_strip.append(triple)

to_ignore = []
for triple in zip(args.ignore-tags,
                  args.ignore-ids,
                  args.ignore-classes):
    to_ignore.append(triple)

to_process = []
for filepath in args.FILES:
    exploredir = ''
    if os.path.isfile(filepath):
        to_process.append(filepath)
    elif os.path.isfile(os.path.join(CURRDIR,filepath)):
        to_process.append(os.path.join(CURRDIR,filepath))
    elif os.path.isdir(filepath):
        exploredir = filepath
    elif os.path.isdir(os.path.join(CURRDIR,filepath)):
        exploredir = os.path.join(CURRDIR,filepath)

    if len(exploredir):
        for f in os.listdir(exploredir):
            if (os.path.isfile(os.path.join(exploredir,f))
                    and os.path.splitext(f)[1] in ['.htm','.html']):
                print(f)
                to_process.append(f)

parser = lxml.etree.HTMLParser(remove_comments=True)
outdir = os.path.join(CURRDIR,'h2dout')
os.mkdir(outdir)
for html_file in to_process:
    doc = lxml.etree.parse(html_file,parser).getroot()
    for tag, idname, classname in to_strip:
        lxml.etree.strip_tags(doc,tag)
        strip_ids(doc,idname)
        strip_classes(doc,classname)
    for tag, idname, classname in to_ignore:
        lxml.etree.ignore_tags(doc,tag)
        ignore_ids(doc,idname)
        ignore_classes(doc,classname)

    remove_tags(doc,'head','link','meta','style','script')
    root = Html_pre(doc)
    lxml.etree.strip_tags(root.element,'body','center','blockquote')
    result = io.StringIO(u'')
    process_element(root,result)

    basename = os.path.splitext(os.path.basename(html_file))[0]
    out = open(os.path.join(outdir,basename + '.txt'),'wb+')
    out.write(result.getvalue().encode('utf-8'))
    out.close()
