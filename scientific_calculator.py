#coding: utf-8



from __future__ import division
import ui
import clipboard
from console import hud_alert
import textwrap
from functools import partial
from textlayout import BuildView

shows_result = False

def f5(sender):
    # Get the button's title for the following logic: =
    '@type sender: ui.Button'
    t = sender.title
    global shows_result
    # Get the labels:
    label = sender.superview['label2']
    label2 = sender.superview['label1']
    try:
        label2.text = label.text + ' ='
        expr = label.text.replace('÷', '/').replace('×', '*')
        label.text = str(eval(expr))
    except SyntaxError:
        label.text = 'ERROR'
    shows_result = True



def f3(sender):
    # Get the button's title for the following logic: 0-9
    '@type sender: ui.Button'
    t = sender.title
    global shows_result
    # Get the labels:
    label = sender.superview['label2']
    label2 = sender.superview['label1']
    if shows_result or label.text == '0':
        # Replace 0 or last result with number:
        label.text = t
    else:
        # Append number:
        label.text += t
    shows_result = False
    label2.text = ''

def f4(sender):
    # Get the button's title for the following logic:+-/*
    '@type sender: ui.Button'
    t = sender.title
    global shows_result
    # Get the labels:
    label = sender.superview['label2']
    label2 = sender.superview['label1']
    label.text += t
    shows_result = False
    label2.text = ''

def f1(sender):
    # Get the button's title for the following logic:ac
    '@type sender: ui.Button'
    #t = sender.title
    global shows_result
    # Get the labels:
    label = sender.superview['label2']
    label2 = sender.superview['label1']
    label.text = '0'
    shows_result = False
    label2.text = ''

def f2(sender):
    # Get the button's title for the following logic:c
    '@type sender: ui.Button'
    t = sender.title
    global shows_result
    # Get the labels:
    label = sender.superview['label2']
    label2 = sender.superview['label1']
    # Delete the last character:
    label.text = label.text[:-1]
    if len(label.text) == 0:
        label.text = '0'
    shows_result = False
    label2.text = ''

def f6(sender):
    # Get the button's title for the following logic:sin
    '@type sender: ui.Button'
    t = sender.title
    global shows_result
    # Get the labels:
    label = sender.superview['label2']
    label2 = sender.superview['label1']
    if shows_result or label.text == '0':
        label.text = t + '('
    else:
        label.text += t + '('
    shows_result = False
    label2.text = ''

from math import *

mem = 0
def mr(sender):
    global mem
    global shows_result
    # Get the labels:
    t = sender.title
    if  t == 'mr':
        t =  str(mem)
    elif t == 'pi':
        t = str(eval(t))
    elif t == 'e':
        t = str(eval(t))
    else:
        t = 'Error'
    label = sender.superview['label2']
    label2 = sender.superview['label1']
    if shows_result or label.text == '0':
        label.text = t
    else:
        label.text += t
    shows_result = False
    label2.text = ''

def ms(sender):
    global mem
    f5(sender)
    mem = eval(sender.superview['label2'].text)


pow10 = lambda x: 10 ** x
powrt = lambda x, y: x ** (1.0 / y)
log10 = lambda x: log(x)/log(10)
mod = lambda x, y: (int(x) % int(y))
deg = lambda x:degrees(x)
rad = lambda x:radians(x)
fe = lambda x:'{:e}'.format(x)
recipro = lambda x:1.0/x
invsign = lambda x:-x
sq = lambda x: x * x
sqrt = lambda x: x ** .5


title = '''\
deg rad ( )  ms           mr  AC C /
pi sin cos tan invsign       7 8 9 *
sq asin acos atan sqrt     4 5 6 -
pow pow10 exp fe  mod       1 2 3 +
powrt log10 log factorial recipro  0 . , =
'''

action = '''\
f6 f6 f4 f4 ms mr f1 f2 f4
mr f6 f6 f6 f6 f3 f3 f3 f4
f6 f6 f6 f6 f6 f3 f3 f3 f4
f6 f6 f6 f6 f6 f3 f3 f3 f4
f6 f6 f6 f6 f6 f3 f3 f3 f5
'''

#print(list(zip(title.strip().split(), action.strip().split())))
title_action_text = '\n'.join([ i+' '+j for i,j in zip(title.strip().split(), action.strip().split())])

layout_text = '''\
l--------
l--------
bbbbbbbbb
bbbbbbbbb
bbbbbbbbb
bbbbbbbbb
bbbbbbbbb
'''

attributes_text = '''\
l text
  0
  0

b title action  
''' + title_action_text


# attributes transformation specification                
attr_transform_map = {
    'action': lambda x:globals()[x] if x in globals() else None
    } 
# Building and presenting main view                                                        
v = BuildView(layout_text, width=800, height=600,
    view_name='Calculator', attributes_text=attributes_text,
    attr_transform_map=attr_transform_map).build_view()      
v.present('popover')
