#coding: utf-8
import ui
from faker import Faker
import clipboard
import console
import editor
import random
import platform
from textlayout import BuildView

view = None

fake = Faker()
seed = random.randint(0, 9999)

def slider_changed(sender):
    fake.seed(seed)
    value1 = int(sender.superview['slider1'].value * 10) + 1
    value2 = int(sender.superview['slider2'].value * 10) + 1
    textview = sender.superview['textview1']
    paragraphs = []
    for i in range(value2):
        p = fake.paragraph(nb_sentences=value1, variable_nb_sentences=True)
        paragraphs.append(p)
    text = '\n\n'.join(paragraphs)
    textview.text = text

def copy_action(sender):
    clipboard.set(sender.superview['textview1'].text)
    console.hud_alert('Copied')

def insert_from_clipboard_action(sender):
    t1 = clipboard.get()
    sender.superview['textview1'].text += '\n' + t1 +'\n'
    
def clear_action(sender):
    sender.superview['textview1'].text = ''
    
def randomize_action(sender):
    global seed
    seed = random.randint(0, 9999)
    slider_changed(sender)

def insert_in_editor_action(sender):
    text = "'''" + sender.superview['textview1'].text + "\n'''"
    start, end = editor.get_selection()
    editor.replace_text(start, end, text)
    if not platform.machine().startswith('iPad'):
        view.close()


layout_text = '''\
l-s--
l-s--
t----
|****
|****
|****
|****
bbbbb
'''

attributes_text = '''\
s action
  slider_changed
  slider_changed

l text
  sentence
  paragraph

b action             title
  copy_action        copy
  randomize_action   randomize
  insert_in_editor_action insert_in_editor
  insert_from_clipboard_action insert_from_clipboard
  clear_action             clear
'''


# attributes transformation specification                
attr_transform_map = {
    'action': lambda x:globals()[x] if x in globals() else None
    } 
# Building and presenting main view                                                        
v = BuildView(layout_text, width=1000, height=600,
    view_name='lorem text generator', attributes_text=attributes_text,
    attr_transform_map=attr_transform_map).build_view() 
slider_changed(v['slider1'])
v.present('popover')
