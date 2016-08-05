# coding: utf-8

from __future__ import division
import ui
import clipboard
from console import hud_alert
import textlayout

shows_result = False

def button_tapped(sender):
    '@type sender: ui.Button'
    # Get the button's title for the following logic:
    t = sender.title
    global shows_result
    # Get the labels:
    label = sender.superview['label1']
    label2 = sender.superview['label2']
    if t in '0123456789':
        if shows_result or label.text == '0':
            # Replace 0 or last result with number:
            label.text = t
        else:
            # Append number:
            label.text += t
    elif t == '.' and label.text[-1] != '.':
        # Append decimal point (if not already there)
        label.text += t
    elif t in '+-÷×':
        if label.text[-1] in '+-÷×':
            # Replace current operator
            label.text = label.text[:-1] + t
        else:
            # Append operator
            label.text += t
    elif t == 'AC':
        # Clear All
        label.text = '0'
    elif t == 'C':
        # Delete the last character:
        label.text = label.text[:-1]
        if len(label.text) == 0:
            label.text = '0'
    elif t == '=':
        # Evaluate the result:
        try:
            label2.text = label.text + ' ='
            expr = label.text.replace('÷', '/').replace('×', '*')
            label.text = str(eval(expr))
        except (SyntaxError, ZeroDivisionError):
            label.text = 'ERROR'
        shows_result = True
    if t != '=':
        shows_result = False
        label2.text = ''

def copy_action(sender):
    '@type sender: ui.Button'
    t1 = sender.superview['label1'].text
    t2 = sender.superview['label2'].text
    text = t2 + ' ' + t1 if t2 else t1
    clipboard.set(text)
    hud_alert('Copied')
   
layout_text = '''
l-------
l-------
b-b-b-b-
b-b-b-b-
b-b-b-b-
b-b-b-b-
b--b--|-
'''


'''attributes = {
    'l':[
        {'text':   '0',
         'background_color': (0.857143,1.000000,0.994286,1.000000) ,  
         'border_color': 'black',
         'flex': 'WHB',
         'alignment': ui.ALIGN_RIGHT
         },
         {'text':   '0',
         'background_color': (0.857143,1.000000,0.994286,1.000000) ,  
         'border_color': 'black',
         'flex': 'WHB',
         'alignment': ui.ALIGN_RIGHT
         }
        ],
    'b':[
        {
          'title': 'AC',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'red',
          'font':('Helvetica', 22)  
        },
        {
          'title': 'C',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'red',
          'font':('Helvetica', 22)  
        },
        {
          'title': '÷',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'blue',
          'font':('Helvetica', 22)  
        },
        {
          'title': '×',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'blue',
          'font':('Helvetica', 22)  
        },
        {
          'title': '7',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '8',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '9',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '-',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'blue',
          'font':('Helvetica', 22)  
        },
        {
          'title': '4',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '5',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '6',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '+',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'blue',
          'font':('Helvetica', 22)  
        },
        {
          'title': '1',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '2',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '3',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '=',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'blue',
          'font':('Helvetica', 22)  
        },
        {
          'title': '0',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        },
        {
          'title': '.',
          'action':button_tapped,
          'border_color':'black',
          'border_width':1,
          'tint_color':'black',
          'font':('Helvetica', 22)  
        }
        ]   
    }
# Building and presenting main view                                                        
v = BuildView(layout_text, width=400, height=350,
    view_name='Calculator', attributes=attributes).build_view() ''' 
    
attributes_text = '''
l text background_color     border_color. flex alignment
  0   (0.857143,1.000000,0.994286,1.000000) black WHB right
  0   (0.857143,1.000000,0.994286,1.000000) black WHB right

b title action border_color border_width tint_color font_size 
AC button_tapped black 1 red 22
C button_tapped black 1 red 22
÷ button_tapped black 1 blue 22
× button_tapped black 1 blue 22
7 button_tapped black 1 black 22
8 button_tapped black 1 black 22
9 button_tapped black 1 black 22
- button_tapped black 1 blue 22
4 button_tapped black 1 black 22
5 button_tapped black 1 black 22
6 button_tapped  black 1 black 22
+ button_tapped black 1 blue 22
1  button_tapped black 1 black 22
2 button_tapped black 1 black 22
3 button_tapped  black 1 black 22
= button_tapped black 1 blue 22
0  button_tapped   black 1 black 22 
. button_tapped black 1 black 22
''' 
# attributes transformation specification                
attr_transform_map = {
        'action': lambda x:globals()[x] if x in globals() else None
        }
                                   
v = textlayout.BuildView(layout_text, width=400, height=350, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view() 
          
v.present('sheet')
