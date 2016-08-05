import ui, textlayout

def button_action(sender):
    label = sender.superview['label1']
    label.text = 'Counter: ' + str(int(label.text.split()[-1]) + 1)

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

'''attributes = {
    'b':[
       {'action':button_action,
         'font' :('Helvetica', 20),
         'title':'Tap to increment counter'
       }],
     'l':[
          {
            'text': 'Counter: 0',
            'alignment':  ui.ALIGN_CENTER,
            'font':('Helvetica', 20)
          }
          ]
         }    
                          
v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
    attributes=attributes).build_view()'''

# attributes specification
attributes_text =    '''
        b background_color   title                      font_name font_size  action        
          whitesmoke        Tap_to_increment_counter    Helvetica 20         button_action  
        
        l background_color   text     alignment font_name font_size
          whitesmoke        Counter:_0 center    Helvetica 20            
        '''         
# attributes transformation specification                
attr_transform_map = {
        'action': lambda x:globals()[x] if x in globals() else None,
        'title': lambda x:x.replace('_', ' '),
        'text': lambda x:x.replace('_', ' ')
        }
                                   
v = textlayout.BuildView(layout_text, width=600, height=600, view_name='Counter',
        attributes_text=attributes_text,
        attr_transform_map=attr_transform_map).build_view()  
          
v.present('popover')
