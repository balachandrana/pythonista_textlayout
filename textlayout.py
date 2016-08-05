# coding: utf-8
"""
A compact text based alternative to pyui

layout_text
  - specifies position and size of each ui elemement
  - lines represent rows in grid and each character represents a grid cell
  - '*' represenrs blank cell
  -  ui elements represented by a single character
                'b': ('button', ui.Button),
                'c': ('switch', ui.Switch),
                'd': ('datepicker', ui.DatePicker),
                'f': ('textfield', ui.TextField),
                'g': ('segmentedcontrol', ui.SegmentedControl),
                'i': ('imageview', ui.ImageView),
                'l': ('label', ui.Label),
                's': ('slider', ui.Slider),
                't': ('textview', ui.TextView),
                'w': ('webview', ui.WebView),
                'V': ('view', ui.View)
    - the characters '-' and '|' are used for horizontal and vertical spanning of grid cells
    
    # sample layout specification 
    # - counter aplication with one label and one button
    # - the label element - single row with four horizontal cells
    # - the button element - a rectangular box of 3*4 cells
    layout_text = '''
    ********
    **l---**
    ********
    ********
    **b---**
    **|--|**
    **|--|**
    ********
    ********
    '''
"""
import ui, textwrap
from copy import copy
import json
import uuid
import os
import re
from ast import literal_eval
import pprint
import io

class LayoutProcessor(object):
    def __init__(self, layout_text,
            width=400, height=600,
            cell_size=None,
            marginx=2, marginy=2,
            ui_element_map=None):
        self.layout_text = layout_text
        self.ui_element_map = ui_element_map
        self.height = height
        self.width = width
        self.marginx = marginx
        self.marginy = marginy
        self.frame_map = None
        self.cell_size = cell_size
        self.size = None
        self.build_frame_map()
               
    def process_layout_text(self):
        self.layout_list = [i for i in textwrap.dedent(self.layout_text).strip().split('\n')]
        self.m = len(self.layout_list)
        self.n = max(len(l) for l in self.layout_list)
        if self.cell_size:
            self.cell_width, self.cell_height = self.cell_size
        else:
            self.cell_width = self.width/self.n
            self.cell_height = self.height/self.m 
            self.cell_size = (self.cell_width, self.cell_height)
        self.size = (self.cell_width*self.n, self.cell_height*self.m)       
        
    def get_frame(self, s, i, j):
        p = j + 1
        while p < len(s[i]) and s[i][p] == '-':
            p += 1
        q = i + 1
        while q < len(s) and s[q][j] == '|':
            q += 1
        x = j * self.cell_width + self.marginx
        y = i * self.cell_height + self.marginy
        h = (q - i) * self.cell_height - 2 * self.marginy
        w = (p - j) * self.cell_width - 2 * self.marginx
        return (x, y, w, h)
    
    def build_frame_map(self):
        self.process_layout_text()
        lines = self.layout_list
        frame_map = {}
        for i, item_i in enumerate(lines):
            for j, item_j in enumerate(item_i):
                if item_j in self.ui_element_map: #'bcdfgilstwV':
                    frame_map.setdefault(item_j, []).append(
                            self.get_frame(lines, i, j))
        self.frame_map = frame_map

class AttributeInitializer(object):
    def __init__(self, attributes_text=None,
            ui_element_map=None,
            attr_transform_map=None,
            attr_transform_uielement_specific_map=None,
            attribute_style='',
            splitchar=None):
        if ui_element_map:
            self.ui_element_map = ui_element_map
        else:
            self.ui_element_map = {}
        self.attributes_text = attributes_text
        self.attr_transform_map = attr_transform_map
        self.attr_transform_uielement_specific_map = attr_transform_uielement_specific_map
        self.splitchar = splitchar # for splitting attributes    
        self.default_attr_transform_map = {
            'alignment': lambda x: ui.ALIGN_LEFT if x == 'left' else (
                ui.ALIGN_RIGHT if x == 'right' else (
                ui.ALIGN_CENTER if x == 'center' else ui.ALIGN_LEFT)),
            'image': lambda x: ui.Image.named(x) if (
                isinstance(x, str)) else x,
            'segments': lambda x:x.split('|'),
            'value': lambda x:literal_eval(x),
            'border_width':lambda x:literal_eval(x),
            'mode':lambda x:literal_eval(x),
            'enabled':lambda x:literal_eval(x),
            'number_of_lines':lambda x:literal_eval(x),
            'line_break_mode': None,
            'selected_index':lambda x:literal_eval(x),
            'continuous':lambda x:literal_eval(x),
            # need to avoid eval, safer to define ui_constants
            'autocapitalization_type':lambda x:eval('ui.'+x), #ui_constants[x],
            #'autocorrection_type':lambda x:literal_eval(x),
            'bordered':lambda x:literal_eval(x),
            'scales_to_fit':lambda x:literal_eval(x)} 
        if attr_transform_map:
            self.default_attr_transform_map.update(attr_transform_map)      
        self.attr_transform_map = self.default_attr_transform_map
        default_attr_transform_uielement_specific_map = {}
        if attr_transform_uielement_specific_map:
            default_attr_transform_uielement_specific_map.update(
                    attr_transform_uielement_specific_map)
        self.attr_transform_uielement_specific_map = (
            default_attr_transform_uielement_specific_map)
        self.default_attribute_style = '''\
                V clsss
                  View
                  
                l class alignment font_name font_size text
                  Label left      <System>  18        Label
                  
                b class  font_size title
                  Button 15        Button
                  
                s class  flex value 
                  Slider W    0.5
                  
                c class  value
                  Switch True
                  
                g class            flex segments
                  SegmentedControl LR  hello|world
                  
                
                f class     alignment autocorrection_type font_name font_size  spellchecking_type
                  TextField left      default             <System>  17         default

                t class    alignment autocorrection_type editable flex  font_name     font_size  spellchecking_type
                  TextView left      default             True     WH   <System>      17             default               
 
                w class   flex scales_to_fit
                  WebView WH   True

                T class background_color data_source_delete_enabled data_source_font_size  data_source_items  flex 
                  TableView (1.0,1.0,1.0,1.0) True 18 Row_1|Row_2|Row_3  WH 

                d class      mode
                  DatePicker 1
                  
                i class
                  ImageView
                  
                v class background_color border_color enabled  tint_color
                  View white black True (0.000000,0.478000,1.000000,1.000000)
                '''
        self.attribute_style = attribute_style
        self.attributes_text = attributes_text
        self.splitchar = splitchar
        self.build_attrdict()
        #print(self.attrdict)

    def parse_attribute_record_text(self, attrrec_text, splitchar=None):
        lines = attrrec_text.strip().split('\n')
        #ch, *attr_names = lines[0].split(splitchar) if splitchar else lines[0].split() #works on 3.5 only
        first_line = lines[0].split(splitchar) if splitchar else lines[0].split()
        ch = first_line[0]
        attr_names = first_line[1:]
        attrrec_list = []
        for line in lines[1:]:
            attrrec = {}
            for i, attr in enumerate(
                    line.split(splitchar) if splitchar else line.split()):
                attrrec[attr_names[i]] = attr
            attrrec_list.append(attrrec)
        return (ch, attrrec_list)
                
    def parse_attributes_text(self, attributes_text, ui_element_map, splitchar=None):
        attrdict = {}
        for ch in ui_element_map:
            attrdict[ch] = []
        if attributes_text:
            attrrecwithschemalist = re.split(r'\n(?:[ \t\n\r]*\n)+', attributes_text.strip()) 
            for attrrecwithschema_text in attrrecwithschemalist:
                ch, attrrec_list = self.parse_attribute_record_text(attrrecwithschema_text,
                    splitchar=splitchar)
                #print(ch)
                attrdict[ch] += attrrec_list       
        return attrdict 
                                                      
    def build_default_attrdict(self, default_attribute_style,
            attribute_style, ui_element_map, splitchar=None):
        self.default_attrdict = self.parse_attributes_text(default_attribute_style,
            ui_element_map, splitchar=splitchar)
        override_attrdict = self.parse_attributes_text(attribute_style,
            ui_element_map, splitchar=splitchar)
        for ch in self.default_attrdict:
            if (ch in override_attrdict) and override_attrdict[ch]:
                d = override_attrdict[ch][0]
                if d:
                    if self.default_attrdict[ch][0]:
                        self.default_atrdict[ch][0].update(d)
                    else:
                        self.default_attrdict[ch][0] = d
                        
    def apply_transformation_to_attrdict(self):
        for ch in self.attrdict:
            for attrrec in self.attrdict[ch]:
                for attr in list(attrrec.keys()):
                    attr_value = attrrec[attr]
                    transform = lambda x:x
                    if attr in self.attr_transform_map:
                        transform = self.attr_transform_map[attr]
                    if ch in self.attr_transform_uielement_specific_map and (
                            attr in self.attr_transform_uielement_specific_map[ch]):
                        transform = self.attr_transform_uielement_specific_map[ch][attr]
                    # special transforms for font and color
                    if attr == 'font_name':
                        attrrec['font'] = attr_value, attrrec.get('font', ('<System>', 17))[1]
                        #del attrrec['font_name']
                    elif attr == 'font_size':
                        attrrec['font'] = attrrec.get('font', ('<System>', 17))[0], int(attr_value)
                        #del attrrec['font_size']
                    elif attr.endswith('color'):
                        if attr_value.startswith('('):
                            attrrec[attr] = literal_eval(attr_value)
                    else:
                        attrrec[attr] = transform(attr_value)  
                                                                                                                              
    def build_attrdict(self):
        self.build_default_attrdict(self.default_attribute_style,
            self.attribute_style,
            self.ui_element_map,
            splitchar=self.splitchar)
        #print(self.default_attrdict)
        attrdict_fromtext = self.parse_attributes_text(self.attributes_text,
            self.ui_element_map, splitchar=self.splitchar)
        self.attrdict = {}
        for ch in attrdict_fromtext:
            self.attrdict[ch] = []
            for attrrec in attrdict_fromtext[ch]:
                if self.default_attrdict[ch]:
                    newrec = self.default_attrdict[ch][0].copy()
                else:
                    newrec = {}
                newrec.update(attrrec)
                self.attrdict[ch].append(newrec)
        # add main view attribute if not there
        if not self.attrdict['v']:
            ch = 'v'
            if self.default_attrdict[ch]:
                newrec = self.default_attrdict[ch][0].copy()
            else:
                newrec = {}
            self.attrdict[ch].append(newrec)
        self.apply_transformation_to_attrdict()
        if self.attrdict['L']:
            self.attrdict['v'][0]['left_button_items'] = [ui.ButtonItem(**d) for d in self.attrdict['L']]
        if self.attrdict['R']:
            self.attrdict['v'][0]['right_button_items'] = [ui.ButtonItem(**d) for d in self.attrdict['R']]
            
class BuildView(object):
    """
            Build view object from layout text and attribute text
    """
    def __init__(self, layout_text,
            position=(0, 0),
            width=400, height=600,
            marginx=2, marginy=2,
            view_name='View',
            attributes=None,
            attributes_text=None,
            attr_transform_map=None,
            attr_transform_uielement_specific_map=None,
            attribute_style='',
            splitchar=None):
        self.ui_element_map = {
                'b': ('button', ui.Button),
                'c': ('switch', ui.Switch),
                'd': ('datepicker', ui.DatePicker),
                'f': ('textfield', ui.TextField),
                'g': ('segmentedcontrol', ui.SegmentedControl),
                'i': ('imageview', ui.ImageView),
                'l': ('label', ui.Label),
                's': ('slider', ui.Slider),
                't': ('textview', ui.TextView),
                'w': ('webview', ui.WebView),
                'T': ('tableview', ui.TableView),
                'L': ('leftbuttonitem', ui.ButtonItem),
                'R': ('rightbuttonitem', ui.ButtonItem),
                'v': ('view', ui.View),  #main view             
                'V': ('view', ui.View) #custom view
                }
        self.view_name = view_name
        self.position = position
        self.width = width
        self.height = height
        self.layout_processor = LayoutProcessor(layout_text,
            width=width, height=height,
            marginx=marginx, marginy=marginy,
            ui_element_map=self.ui_element_map)
        self.frame_map = self.layout_processor.frame_map
        self.attribute_initializer = AttributeInitializer(attributes_text=attributes_text,
            ui_element_map=self.ui_element_map,
            attr_transform_map=attr_transform_map,
            attr_transform_uielement_specific_map=attr_transform_uielement_specific_map,
            attribute_style=attribute_style,
            splitchar=splitchar)
        self.attrdict = self.attribute_initializer.attrdict
        if attributes:
            self.attributes = {elem: attributes.get(elem, [])
                           for elem in self.ui_element_map} 
        else:
            self.attributes = {elem: self.attrdict.get(elem, [])
                           for elem in self.ui_element_map}
                                                          
    def build_node(self, class_char, idx, frame, attributes=None):
        name, ui_element = self.ui_element_map[class_char]
        index = idx + 1
        v = ui_element(name=((name)+ str(index)))
        v.frame = frame
        for attr in attributes or []:
            #print(attr, attributes[attr], type(attributes[attr]))
            setattr(v, attr, attributes[attr])
        return v  

    def build_main_view_node(self, frame=(0, 0, 100, 100), attributes=None):
        v = self.build_node('V', -1, frame, attributes)
        v.name = self.view_name         
        return v    
                        
    def build_view(self):
        view_attr = self.attributes.get('v', None)
        view_attr = view_attr[0] if view_attr else None
        main_view_node = self.build_main_view_node((self.position[0],
            self.position[1], self.width, self.height), view_attr)
        for ch in self.frame_map:
            for i, frame in enumerate(self.frame_map[ch]):
                node_attr =  self.attributes[ch][i] if (
                    ch in self.attributes and i in range(
                        len(self.attributes[ch]))) else None
                node = self.build_node(ch, i, frame, node_attr)
                main_view_node.add_subview(node)
        return main_view_node
              
if __name__ == '__main__':
    cnt = 0
    def button_action(sender):
        global cnt
        cnt += 1
        sender.superview['label1'].text = 'Counter:' + str(cnt)

    layout_text = '''
    ********
    **l---**
    ********
    ********
    **b---**
    **|--|**
    **|--|**
    ********
    ********
    '''

    # attributes specification
    attributes_text =    '''\
        b background_color   title                      font_name font_size  action        
          whitesmoke        Tap_to_increment_counter    Helvetica 20         button_action  
        
        l background_color   text     alignment font_name font_size
          whitesmoke        Counter:0 center    Helvetica 20  
          
        ''' 

    # attributes transformation specification                
    attr_transform_map = {
        'action': lambda x:globals()[x] if x in globals() else None,
        'title': lambda x:x.replace('_', ' ')
        }
                
    '''attributes = {
        'b':[
           {'action':button_action,
             'font' :('Helvetica', 20),
             'title':'Tap to increment counter'
           }],
         'l':[
              {
                'text': 'Counter:0',
                'alignment':  ui.ALIGN_CENTER,
                'font':('Helvetica', 20)
              }
              ]
             } 
v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
    attributes=attributes).build_view()'''    
                 
    v = BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()
    v.present('popover')
