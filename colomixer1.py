#coding: utf-8
# ColorMixer
# A simple RGB color mixer with three sliders.

import ui
import clipboard
import textwrap
from random import random
from console import hud_alert
from textlayout import BuildView
from ast import literal_eval

def slider_action(sender):
    # Get the root view:
    v = sender.superview
    # Get the sliders:
    r = v['slider1'].value
    g = v['slider2'].value
    b = v['slider3'].value
    # Create the new color from the slider values:
    v['view1'].background_color = (r, g, b)
    v['label1'].text = '#%.02X%.02X%.02X' % (int(r*255), int(g*255), int(b*255))

def copy_action(sender):
    clipboard.set(sender.superview['label1'].text)
    hud_alert('Copied')

def shuffle_action(sender):
    v = sender.superview
    s1 = v['slider1']
    s2 = v['slider2']
    s3 = v['slider3']
    s1.value = random()
    s2.value = random()
    s3.value = random()
    slider_action(s1)

    
def color_action(sender):
    v = sender.superview
    v['view1'].background_color = t = sender.background_color
    t = (int(t[0]*255), int(t[1]*255), int(t[2]*255))
    v['label1'].text = '#%.02X%.02X%.02X' % t
    v['slider1'].value, v['slider2'].value, v['slider3'].value, a = sender.background_color

layout_text = '''\
                    V-l-
                    s---
                    s---
                    s---
                    bbbb
                    bbbb
                    bbbb
                    bbbb
                    b-b-
                    '''



attributes_text =  '''\
        s background_color   tint_color    action
          whitesmoke         red           slider_action
          whitesmoke         green         slider_action
          whitesmoke         blue          slider_action

         b background_color   title         action  
           aqua               _             color_action      
           black               _             color_action 
           blue               _             color_action   
           fuchsia               _             color_action
           gray               _             color_action
           green               _             color_action
           lime               _             color_action
           maroon               _             color_action
           navy               _             color_action
           olive               _             color_action
           purple               _             color_action
           red               _             color_action
           silver               _             color_action
           teal               _             color_action
           white               _             color_action
           yellow               _             color_action
           whitesmoke         shuffle       shuffle_action  
           whitesmoke         copy          copy_action        

         l background_color   alignment 
           whitesmoke        center    
         
         V background_color   
           whitesmoke                                  
        '''


# attributes transformation specification                
attr_transform_map = {
    'action': lambda x:globals()[x] if x in globals() else None,
    'title': lambda x:x.replace('_', ' ')
    } 
# Building and presenting main view                                                        
v = BuildView(layout_text, width=400, height=350,
    view_name='Color Mixer', attributes_text=attributes_text,
    attr_transform_map=attr_transform_map).build_view() 
v.background_color = 'white'
v.name = 'Color mixer'
slider_action(v['slider1'])   
v.present('popover')
