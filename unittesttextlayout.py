# coding: utf-8
#from __future__ import division
import ui
import textlayout

# attributes transformation specification                
attr_transform_map = {
        'action': lambda x:globals()[x] if x in globals() else None
        }
                                   

    
test_num = 11
if test_num == 1:
    cnt = 0
    def button_action(sender):
        global cnt
        cnt += 1
        sender.superview['label1'].text = 'Counter:' + str(cnt)

    layout_text = '''\
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
    attributes_text =    '''\
                     b background_color   title                      font_name font_size  action        
                       whitesmoke         Tap_to_increment_counter   Helvetica 20         button_action  
            
                     l background_color   text       alignment font_name font_size
                       whitesmoke         Counter:0  center    Helvetica 20   
                    '''  
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()                              
    v.present('popover')

elif test_num == 2:
    def slider_action(sender):
        sender.superview['label1'].text = 'Counter:' + str(
            int(sender.superview['slider1'].value*100))

    layout_text = '''\
    ********
    **l---**
    ********
    **l---**
    **s---**
    **|--|**
    **|--|**
    ********
    ********
    '''

    attributes_text =    '''\
                     s  action        
                        slider_action  
            
                     l background_color   text                    alignment font_name font_size
                       whitesmoke         Counter:0               center    Helvetica 20  
                       white              slide_to_change_counter center    Helvetica 20 
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()                              
    v.present('popover')
elif test_num == 3:    
    def textfield_action(sender):
        sender.superview['label1'].text = 'Counter:' + str(
            sender.superview['textfield1'].text)

    layout_text = '''\
    ********
    **l---**
    ********
    **l---**
    **f---**
    **|--|**
    **|--|**
    ********
    ********
    '''
    attributes_text =    '''\
                     f  action        
                        textfield_action  
            
                     l background_color  text                    alignment font_name font_size
                       whitesmoke        Counter:0               center    Helvetica 20  
                       white             enter_to_change_counter center    Helvetica 20  
                    ''' 

    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()   
    v.present('popover')
elif test_num == 4:    
    def switch_action(sender):
        sender.superview['label1'].text = 'Counter:' + str(
            int(sender.superview['switch1'].value))

    layout_text = '''\
    ********
    **l---**
    ********
    **l---**
    **c---**
    **|--|**
    **|--|**
    ********
    ********
    '''
    attributes_text =    '''\
                     c  action        
                        switch_action  
            
                     l background_color  text                    alignment font_name font_size
                       whitesmoke        Counter:0               center    Helvetica 20  
                       white             slide_to_change_counter center    Helvetica 20  
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()   
    v.present('popover')
elif test_num == 5:    
    def segmentedcontrol_action(sender):
        sc = sender.superview['segmentedcontrol1']
        segments_list = sc.segments
        selected_text = segments_list[sc.selected_index]
        sender.superview['label1'].text = 'Counter:' + selected_text

    layout_text = '''\
    ********
    **l---**
    ********
    **l---**
    **g---**
    **|--|**
    **|--|**
    ********
    ********
    '''
    attributes_text =    '''\
                     g  action                    segments
                        segmentedcontrol_action   100|200|300
            
                     l background_color   text                     alignment font_name font_size
                       whitesmoke         Counter:0                center    Helvetica 20 
                       white              select_to_change_counter center    Helvetica 20    
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()   
    v.present('popover')
elif test_num == 6:    
    def datepicker_action(sender):
        sender.superview['label1'].text = 'Date:' + str(
            sender.superview['datepicker1'].date)

    layout_text = '''\
    ********
    **l---**
    ********
    **l---**
    **d---**
    **|--|**
    **|--|**
    ********
    ********
    '''
    attributes_text =    '''\
                     d  action        
                        datepicker_action  
            
                     l background_color   text            alignment font_name font_size
                       whitesmoke         Date:            center    Helvetica 20 
                       white              enter_date      center    Helvetica 20    
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()   
    v.present('popover')
elif test_num == 7:    
    def segmentedcontrol_action(sender):
        sc = sender.superview['segmentedcontrol1']
        image_list = [ui.Image.named(i) for i in sc.segments]
        sender.superview['imageview1'].image = image_list[sc.selected_index]
        
    layout_text = '''\
    ********
    **i---**
    **|--|**
    **|--|**
    **|--|**    
    ********
    ********
    g-------
    ********
    ********
    '''
    attributes_text =    '''\
                     g  action                   segments
                        segmentedcontrol_action  Rabbit_Face|Mouse_Face|Cat_Face|Dog_Face|Octopus
            
                     i image
                       Rabbit_Face
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()   
    v.present('popover')
elif test_num == 8:    
    def segmentedcontrol_action(sender):
        sc = sender.superview['segmentedcontrol1']
        item_list = [('html', '<!DOCTYPE html><html><body><h1>My Second Heading</h1></html>'),
        ('html', '<!DOCTYPE html><html><body><h1>My First Heading</h1></html>'),
('html','''<html>
  <head>
    <title>my html</title>
  </head>
  <body>
    <h1>h1</h1>
    <h2>h2</h2>
    <h3>h3</h3>
    This is <b>bold</b> text.
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1">
      <rect width="150" height="150" fill="rgb(0, 255, 0)" stroke-width="1" stroke="rgb(0, 0, 0)" />
    </svg>
  </body>
</html>''')
]
        item_type, item = item_list[sc.selected_index]
        if item_type == 'html':
            sender.superview['webview1'].load_html(item)
        elif item_type == 'url':
            sender.superview['webview1'].load_url(item)
        
    layout_text = '''\
    ********
    **w---**
    **|--|**
    **|--|**
    **|--|**    
    ********
    ********
    g-------
    ********
    ********
    '''
    attributes_text =    '''\
                     g  action                   segments 
                        segmentedcontrol_action  html1|html2|html3
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()   
    v.present('popover')
elif test_num == 9: 
    text1 = '"text one" is selected'
    text2 = '"text two" is selected'
    def segmentedcontrol_action(sender):
        sc = sender.superview['segmentedcontrol1']
        item_list = [text1, text2]
        item = item_list[sc.selected_index]
        sender.superview['textview1'].text = item
      
    layout_text = '''\
    ********
    **t---**
    **|--|**
    **|--|**
    **|--|**    
    ********
    ********
    g-------
    ********
    ********
    '''
    attributes_text =    '''\
                     g  action         segments     
                        segmentedcontrol_action  text1|text2
            
                     t text
                        initial_text
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()   
    v.present('popover')
elif test_num == 10:   
    def segmentedcontrol_action(sender):
        sc = sender.superview['segmentedcontrol1']
        color_list = ['red', 'blue', 'yellow', 'green', 'gray']
        sender.superview['view1'].background_color = color_list[sc.selected_index]
       
    layout_text = '''\
    ********
    **V---**
    **|--|**
    **|--|**
    **|--|**    
    ********
    ********
    g-------
    ********
    ********
    '''
    attributes_text =    '''\
                     g  action                   segments
                        segmentedcontrol_action  red|blue|yellow|green|gray
            
                     i image
                       Rabbit_Face
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()   
    segmentedcontrol_action(v['segmentedcontrol1']) 
    v.present('popover')
elif test_num == 11:
    # layout specification
    layout_text = '''\
    ********
    **l---**
    ********
    ********
    **T---**
    **|--|**
    **|--|**
    ********
    ********
    '''
    # attributes specification
    attributes_text =    '''\
                     T background_color  data_source_items
                       whitesmoke    aaaa\nbbbbb\ncccc    
            
                     l background_color   text     alignment font_name font_size
                       whitesmoke        Counter:0 center    Helvetica 20   
                    ''' 
    v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()       
    v.present('popover')
