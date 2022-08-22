#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 16:26:35 2022

@author: jpbakken
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 15:09:47 2022

@author: jpbakken
"""
import json
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivy.uix.label import Label
from kivymd.uix.snackbar import Snackbar
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from itertools import compress
import kv





class MainApp(MDApp):

# =============================================================================
# data methods
# =============================================================================
    '''
    Project structure:
    self.projects = 
        {'Project Name': {
            'Pieces': {
                'Piece Name': [steps list],
                'Other Piece': [steps list],
               }
            },
            'Substeps': {
                'Piece Name': [substeps list],
                'Other Piece': [substeps list],
                }
            }
    '''
    def set_data_dir(self):
        app = MDApp.get_running_app()
        self.data_dir = app.user_data_dir


    def write_projects(self):
        
        with open(self.data_dir + '/projects.json', 'w') as f:
            json.dump(self.projects, f)
            
        self.read_projects()

    def read_projects(self):
        try:
            with open(self.data_dir + '/projects.json') as json_file:     
                  self.projects = json.load(json_file)
        except:
            with open('data/projects.json') as json_file:     
                  self.projects = json.load(json_file)
             
    def wk_project_vars(self,project_name):
        '''
        set working project variables
        '''        
        self.wk_project = self.projects[project_name]
        self.wk_project_name = project_name

        self.toolbar_title = project_name        
        self.screen_name = self.ProjectScreenName

        self.wk_pieces = self.wk_project['Pieces'].keys()
        
    def wk_piece_vars(self,piece_name):
        
        self.toolbar_title = self.wk_project_name + ': ' + piece_name
        self.screen_name = self.PieceScreenName

        self.wk_piece_name = piece_name
        self.wk_piece = self.wk_project['Pieces'][piece_name]
        self.wk_step = self.wk_piece[0]

# =============================================================================
# class variables
# =============================================================================

    def set_vars_layout(self):
        '''
        define variables that are used in layouts
        '''
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"


        self.root= Builder.load_string(kv.screen)
        self.step_edit_layout = Builder.load_string(kv.step_edit_screen)


    def set_vars(self):
        """
        Define variables that can be used throughout
        """
        self.set_data_dir()

        self.menu_item_settings = 'Settings'

        self.project_menu_item_1 = 'Add Piece'
        self.project_menu_item_2 = 'Back to Projects'
        self.project_menu_item_3 = 'Clear Box Widget'
        
        
        self.project_menu_labels = [self.project_menu_item_1,
                                    self.project_menu_item_2,
                                    self.project_menu_item_3,
                                    self.menu_item_settings
                                    ]

        self.piece_menu_item_1 = 'Add Step'
        self.piece_menu_item_2 = 'Back to Project Pieces'
        
        self.piece_menu_labels = [self.piece_menu_item_1,
                                  self.piece_menu_item_2,
                                  self.menu_item_settings]
        
        self.root_menu_item_1 = 'New Project'
        self.root_menu_item_2 = 'Clear Box Widget'

        self.root_menu_labels = [self.root_menu_item_1,
                                 self.root_menu_item_2,
                                  self.menu_item_settings]
        
        self.toolbar_title = 'Projects'
        
        self.ListScreenName = 'list'
        self.TableScreenName = 'table'
        self.StepEditScreenName = 'stepedit'
        
        self.RootScreenName = 'root'
        self.ProjectScreenName = 'project'
        self.PieceScreenName = 'pice'

# =============================================================================
# gui build - general
# =============================================================================
    def widget_hide(self, widget):
        widget.disabled = True
        widget.opacity = 0
        widget.clear_widgets()
        
    def widget_visible(self,widget):
        widget.clear_widgets()
        widget.disabled = False
        widget.opacity = 1

# =============================================================================
# gui build - menu
# =============================================================================
    def menu_open(self, button):
        self.menu.caller = button
        self.menu.open()


    def menu_callback(self, text_item):
        self.menu.dismiss()
        
        if text_item == 'Settings':
            self.open_settings()
                    
        elif self.screen_name == self.RootScreenName:
            self.root_menu_callback(text_item)

        elif self.screen_name == self.ProjectScreenName:
            self.project_menu_callback(text_item)

        elif self.screen_name == self.PieceScreenName:
            self.piece_menu_callback(text_item)

        else:
            Snackbar(text=text_item).open()


    def menu_build(self, menu_labels):
        '''
        '''
        
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(56),
                "on_release": lambda x=i: self.menu_callback(x),
              } for i in menu_labels
        ]
        
        self.menu = MDDropdownMenu(items=menu_items,
                                        width_mult=4)
        
        # set action items for the menu
        self.root.ids.toolbar.left_action_items = [
            ["menu", lambda x: self.menu_open(x)]]
        
        self.root.ids.toolbar.title = self.toolbar_title

# =============================================================================
# gui build - list of items in scrollview
# =============================================================================

    def list_build(self,items):
        '''
        '''
        
        # show an empty content area
        self.widget_visible(self.root.ids.content)
        
        # create list and add the items
        mdlist = MDList()        

        # iterate through items and build the scroll list
        for i in items:
            mdlist.add_widget(
                OneLineListItem(
                    text="{}".format(i),
                    on_release=lambda x=i: self.list_on_release(x.text),))
                        
        # add list to the scroll view
        scroll = ScrollView()
        scroll.add_widget(mdlist)

        # add widget to the content area
        self.root.ids.content.add_widget(scroll)


    def list_on_release(self, text_item):
        '''
        what to do when an item in the list object is released
        
        self.screen_name is set in the _build functions for each screen
        '''
        
        if self.screen_name == self.RootScreenName:
            self.project_build(text_item)
            
        elif self.screen_name == self.ProjectScreenName:
            self.piece_build(text_item)
        
        else:
            Snackbar(text=text_item).open()


# =============================================================================
# gui build - root screen
# =============================================================================
    def root_build(self):
        '''
        build the root screen:
            -- set toolbar title and menu items
            -- build scroll list and fill with projects
            
        self.screen_name is used in functions that determine 
            what happens when list item and menus are clicked 
        '''
        self.screen_name = self.RootScreenName  
        self.toolbar_title = 'Projects'

        self.read_projects()
        
        self.menu_build(self.root_menu_labels)
        
        self.list_build(self.projects.keys())


# =============================================================================
# gui build - project page (listing pices)
# =============================================================================

    def project_build(self, project_name):
        '''
        build the working project screen
            -- set toolbar title and menu items
            -- build scroll list and fill with pieces
            
        self.screen_name is used in functions that determine 
            what happens when list item and menus are clicked 

        '''
        # set variables for the selected working project
        self.wk_project_vars(project_name)

        # update the toolbar title and menu items
        self.menu_build(self.project_menu_labels)            

        # rebuild self.root.ids.list
        self.list_build(self.wk_pieces)
        
        
    def project_menu_callback(self, text_item):
        
        if text_item == 'Back to Projects':
            self.root_build()

        else:
            Snackbar(text=text_item).open()

# =============================================================================
# gui build - piece page (listing steps)    
# =============================================================================
    def piece_build(self, piece_name):
        '''
        '''
        # set variables for the selected working piece
        self.wk_piece_vars(piece_name)
        
        # update the toolbar title and menu items
        self.menu_build(self.piece_menu_labels) 

        # show and clear anything left in the widget
        self.widget_visible(self.root.ids.content)
        
        
        # self.root.ids.content.add_widget(MDGridLayout(cols=1))
        
        # create the containers for displaying piece edit screens
        self.piece_cols = MDGridLayout(cols = 3)
        self.piece_lcol = MDGridLayout(size_hint = (.2,1),
                                       cols = 1,)

        self.piece_cols.add_widget(self.piece_lcol)
        
        # add box for padding buffer
        self.piece_cols.add_widget(MDBoxLayout(size_hint = (.05,1)))

        self.piece_rcol = MDBoxLayout(
            # md_bg_color = self.theme_cls.primary_light,
            )       
        self.piece_cols.add_widget(self.piece_rcol)

                
        # build the code buttons and edit screen
        self.steps_code_list_build()
        self.step_edit_build()
        
        # add widget to the content area
        self.root.ids.content.add_widget(self.piece_cols)


    def piece_menu_callback(self, text_item):
    
        if text_item == 'Back to Project Pieces':
            self.project_build(self.wk_project_name)
        
        else:
            Snackbar(text=text_item).open()



    def steps_code_list_build(self):
                
        # show and clear anything left in the widget
        self.widget_visible(self.piece_lcol)

        # create list and add the items
        mdlist = MDList()     
        
        for piece in self.wk_piece:
            
            code = piece['Code']
            
            button = MDRaisedButton(
                        text=code,
                        # md_bg_color=self.theme_cls.primary_dark,
                        size_hint = (1,.8),
                        on_release = lambda x=code: self.step_edit(x.text))
                    
            mdlist.add_widget(button)
                    
        # add list to the scroll view
        scroll = ScrollView()
        scroll.add_widget(mdlist)
        
        self.piece_lcol.add_widget(scroll)
        
       
        return 

    def step_edit(self,step_code):
        '''
        screen to edit or delete a step
        '''        
        # save the values of the current step before switching
        self.step_save()
        
        if self.validation_error == False:
            self.step_set_text(step_code)
            
        
    def step_edit_build(self):

        # show and clear anything left in the widget
        self.widget_visible(self.piece_rcol)
        
        # set the header and content layout and 
        self.piece_rcol.add_widget(self.step_edit_layout)     
        self.root.ids.header.text = 'Edit piece: ' + self.wk_step['Code']

        self.step_set_text(self.wk_step['Code'])        

        # # get the step data for the current step
        # current_step = [ sub['Code'] == self.wk_step['Code'] for sub in self.wk_piece ]
        # self.wk_step = list(compress(self.wk_piece, current_step))[0]
        
        # # set text box values based on the step
        # self.step_set_text()        

        
    def step_set_text(self, step_code):
        '''
        set peice to saved values
        '''
        
        # get the dict values for the selected step
        current_step = [ sub['Code'] == step_code for sub in self.wk_piece ]
        wk_step = list(compress(self.wk_piece, current_step))
        self.wk_step = wk_step[0]

        step = self.wk_step
        
        self.step_edit_layout.ids.code_entry.text = step['Code']
        self.step_edit_layout.ids.action_entry.text = step['Action']
        self.step_edit_layout.ids.start_entry.text = str(step['StartRow'])
        self.step_edit_layout.ids.times_entry.text = str(step['HowManyTimes'])
        self.step_edit_layout.ids.often_entry.text = str(step['HowOften'])
        self.step_edit_layout.ids.font_entry.text = step['FontColor']

    def step_int_type_check(self):

        self.validation_error = False

        if self.step_edit_layout.ids.start_entry.text.isnumeric() == False:
            self.step_edit_layout.ids.start_entry.error = True
            self.validation_error = True
        if self.step_edit_layout.ids.often_entry.text.isnumeric() == False:
            self.step_edit_layout.ids.often_entry.error = True
            self.validation_error = True
        if self.step_edit_layout.ids.times_entry.text.isnumeric() == False:
            self.step_edit_layout.ids.times_entry.error = True
            self.validation_error = True

            return 

    def step_save(self):
        
        step = self.wk_step
        
        self.step_int_type_check()
        
        if (self.step_edit_layout.ids.start_entry.error == False and 
            self.step_edit_layout.ids.often_entry.error == False and 
            self.step_edit_layout.ids.times_entry.error == False):
            
            step['Code'] = self.step_edit_layout.ids.code_entry.text
            step['Action'] = self.step_edit_layout.ids.action_entry.text
            step['StartRow'] = int(self.step_edit_layout.ids.start_entry.text)
            step['HowManyTimes'] = int(self.step_edit_layout.ids.times_entry.text)
            step['HowOften'] = int(self.step_edit_layout.ids.often_entry.text)
            step['FontColor'] = self.step_edit_layout.ids.font_entry.text
            
            self.write_projects()  

        
        
# =============================================================================
# build application
# =============================================================================
    def build(self):
        self.set_vars()   
        self.set_vars_layout()

        
        self.root_build()
        


if __name__ == '__main__':
    MainApp().run()