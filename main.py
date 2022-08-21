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
from kivy.uix.label import Label
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.gridlayout import MDGridLayout
from itertools import compress
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton


# from kivymd.uix.floatlayout import MDFloatLayout
# from kivymd.uix.datatables import MDDataTable
# from kivy.properties import ObjectProperty
# from kivy.uix.screenmanager import ScreenManager
# from kivymd.uix.scrollview import ScrollView
# froxm kivymd.uix.scrollview import MDScrollView
# from kivymd.uix.screen import MDScreen
# from kivy.uix.settings import Settings
# import pandas as pd
# from kivymd.uix.tab import MDTabsBase
kv = '''

<AppScreen>:

    MDTopAppBar:
        id: toolbar
        title: 'Projects'
        pos_hint: {'center_x':0.5, 'top':1}

    ScreenManager:
        id: sm
        ListScreen:
        TableScreen:
        StepEditScreen:



<ListScreen>:
    name: 'list'
    
    MDBoxLayout:  
        id: box
        size_hint: (.9, .6)
        pos_hint: {'center_x':.5, 'center_y':.5}
        
        ScrollView:
            MDList:
                id: list   

<TableScreen>:
    name: 'table'

    MDBoxLayout:  
        id:box
        size_hint: (.9, .6)
        pos_hint: {'center_x':.5, 'center_y':.5}

        ScrollView:
            MDList:
                id: list   
                
<StepEditScreen>:
    name: 'stepedit'

    MDFloatLayout:  
        id:float
        size_hint: (.9, .8)
        pos_hint: {'center_x':.5, 'center_y':.5}
                    
        MDGridLayout:
            id: list_grid
            cols: 1
            size_hint: (.6,.8)
            pos_hint: {'center_x': .5, 'center_y': .5}
                
            MDTextField: 
                id: code_entry
                hint_text: 'Code'
                helper_text: 'There can be only one...code must be unique'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                #size_hint_x: None
                width: 200
            MDTextField: 
                id: action_entry
                hint_text: 'Action'
                helper_text: 'Desribe the step'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                #size_hint_x: None
                width: 200
            MDTextField: 
                id: start_entry
                hint_text: 'Start Row'
                helper_text: 'Start row must be a number'
                helper_text_mode: 'on_error'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                #size_hint_x: None
                width: 200
                on_text_validate: app.step_int_type_check
                
            MDTextField: 
                id: often_entry
                hint_text: 'How Often to repeat the step'
                helper_text: 'How often must be a number'
                helper_text_mode: 'on_error'                
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                #size_hint_x: None
                width: 200
            MDTextField: 
                id: times_entry
                hint_text: 'How Many Times to repeat the step'
                helper_text: 'How many times must be a number'
                helper_text_mode: 'on_error'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                #size_hint_x: None
                width: 200
            MDTextField: 
                id: font_entry
                hint_text: 'Font Color'
                helper_text: 'Font color for the step when working the project'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                #size_hint_x: None
                width: 200

            MDGridLayout:
                id: list_grid
                cols: 3
                size_hint: (1,.1)
                #pos_hint: {'center_x': .5, 'center_y': .2}
                col_default_width: self.width/3
                col_default_height: self.height

    
                MDRaisedButton:
                    text: 'Save Step'
                    pos_hint: {'center_x': 0, 'center_y': .1}
                    md_bg_color: app.theme_cls.primary_dark
                    on_release: app.step_save(app.wk_step[0])

                MDRaisedButton:
                    text: 'Reset Values'
                    pos_hint: {'center_x': .5, 'center_y': .1}
                    md_bg_color: app.theme_cls.primary_dark
                    on_release: app.step_set_text(app.wk_step[0])

                MDRaisedButton:
                    text: 'Exit'
                    pos_hint: {'x': 1, 'center_y': .1}
                    md_bg_color: app.theme_cls.primary_dark
                    on_release: app.step_exit()
'''



Builder.load_string(kv)

class AppScreen(Screen):
    pass

class ListScreen(Screen):
    pass

class TableScreen(Screen):
    pass

class StepEditScreen(Screen):
    pass

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
    def write_projects(self):
        
        with open('data/projects.json', 'w') as f:
            json.dump(self.projects, f)
            
        self.read_projects()

    def read_projects(self):
         
        with open('data/projects.json') as json_file:     
             self.projects = json.load(json_file)
             
    def wk_project_vars(self,project_name):
        '''
        set working project variables
        '''        
        self.wk_project = self.projects[project_name]
        self.wk_project_name = project_name
        self.toolbar_title = project_name
        
        self.wk_pieces = self.wk_project['Pieces'].keys()
        
    def wk_piece_vars(self,piece_name):
        
        self.toolbar_title = self.wk_project_name + ': ' + piece_name
        self.wk_piece_name = piece_name

             
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

    def set_screen(self, screen_name):
        self.root.ids.sm.current = screen_name
        
# =============================================================================
# gui build - menu
# =============================================================================
    def set_vars(self):
        """
        Define variables that can be used throughout
        """
        self.project_menu_labels = ['Add Piece',
                                    'Back to Projects',
                                    'Clear Box Widget',
                                    'Settings']

        self.piece_menu_labels = ['Add Step',
                                    'Back to Pieces',
                                    'Settings']
        
        self.root_menu_labels = ['New Project',
                                    'Clear Box Widget',
                                 'Settings']
        
        self.toolbar_title = 'Projects'
        
        self.ListScreenName = 'list'
        self.TableScreenName = 'table'
        self.StepEditScreenName = 'stepedit'
        
        self.RootScreenName = 'root'
        self.ProjectScreenName = 'project'
        self.PieceScreenName = 'pice'


    def menu_open(self, button):
        self.menu.caller = button
        self.menu.open()


    def menu_callback(self, text_item):
        self.menu.dismiss()
        
        if text_item == 'Settings':
            self.open_settings()
        
        # elif self.screen_name == 'root':
        #     self.widget_hide(self.screen_list.ids.list)
            
        elif text_item in self.root_menu_labels:
            self.root_menu_callback(text_item)

        elif text_item in self.project_menu_labels:
            self.project_menu_callback(text_item)
            
        # else:
        #     Snackbar(text=text_item).open()

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
        
        # show the empty scroll list
        self.widget_visible(self.screen_list.ids.list)

        # iterate through items and build the scroll list
        for i in items:
            self.screen_list.ids.list.add_widget(
                OneLineListItem(
                    text="{}".format(i),
                    on_release=lambda x=i: self.list_on_release(x.text),))
            
            
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
# gui build - table list
# =============================================================================

    def steps_table_build(self,items):
        '''
        '''
        
        # show the empty scroll list
        self.widget_visible(self.screen_table.ids.list)



        # iterate through items and build the scroll list
        for i in items:
            
            code = i['Code']
            code_col_size = (.2, 1)
            action = i['Action']
            action_col_size = (1,1)
            start_row = str(i['StartRow'])
            times = str(i['HowManyTimes'])
            often = str(i['HowOften'])
            color = i['FontColor']
            
            grid = MDGridLayout(cols=4,
                                )
            #  add code button
            box = self.steps_table_col_box(code_col_size)
            
            box.add_widget(MDRaisedButton(
                text=code,
                md_bg_color=self.theme_cls.primary_dark,
                size_hint = (1,.8),
                on_release = lambda x=code: self.step_edit(x.text)))
            grid.add_widget(box)
            
            box = self.steps_table_col_box(action_col_size)
            box.add_widget(Label(text=action))
            grid.add_widget(box)


            # grid = self.steps_table_col_add(grid, code, code_col_size,True)

            # grid = self.steps_table_col_add(grid, action, action_col_size)


            # grid.add_widget(Label(text=action))
            grid.add_widget(Label(text=times))
            grid.add_widget(Label(text=often))

            # row = i['Code'] + ' ' * (30 - len(i['Code'])) + i['Action']
            # self.screen_table.ids.action.text = i['Action']
            # self.screen_table.ids.code.text = i['Code']

            self.screen_table.ids.list.add_widget(grid)
            
            # self.screen_table.ids.list.add_widget(
            #     OneLineListItem(
            #         text="{}".format(row),
            #         on_release=lambda x=i['Code']: self.list_on_release(x.text),))

    def steps_table_col_add(self,grid,text,col_size, button=False):
        
        box = self.steps_table_col_box(col_size)
        box.add_widget(self.steps_table_col(text,button))
        grid.add_widget(box)
        
        return grid

        
    def steps_table_col_box(self,size):
        
            return MDBoxLayout(size_hint= size,
                               pos_hint={"left": 1, "y": 0})
        
        
    def steps_table_col(self, text, button=False):
        
        if button:
            
            return MDRaisedButton(
                text=text,
                md_bg_color=self.theme_cls.primary_dark,
                size_hint = (1,.8),
                on_release = lambda x=text: self.step_edit(x.text))
        
        else:
            return Label(text=text,
                         size_hint = (1,.8))


    def step_new(self):
        '''
        create a new step
        '''
        # TODO: make sure codes are unique

    def step_code_unique_check(self):
        '''
        check to make sure the entered code doesn't already exists
        '''
        
        
    def step_edit(self,step_code):
        '''
        screen to edit or delete a step
        input: unique step code
        
        '''
        # activate the step edit screen
        self.set_screen(self.StepEditScreenName)
        
        # get the dict values for the selected step
        current_step = [ sub['Code'] == step_code for sub in self.wk_piece ]
        self.wk_step = list(compress(self.wk_piece, current_step))
        step = self.wk_step[0]
        
        # set text box values based on the step
        self.step_set_text(step)        

    def step_set_text(self,step):
        '''
        set peice to saved values
        '''
        self.screen_step_edit.ids.code_entry.text = step['Code']
        self.screen_step_edit.ids.action_entry.text = step['Action']
        self.screen_step_edit.ids.start_entry.text = str(step['StartRow'])
        self.screen_step_edit.ids.times_entry.text = str(step['HowManyTimes'])
        self.screen_step_edit.ids.often_entry.text = str(step['HowOften'])
        self.screen_step_edit.ids.font_entry.text = step['FontColor']


    def step_int_type_check(self):

        if self.screen_step_edit.ids.start_entry.text.isnumeric() == False:
            self.screen_step_edit.ids.start_entry.error = True

        if self.screen_step_edit.ids.often_entry.text.isnumeric() == False:
            self.screen_step_edit.ids.often_entry.error = True

        if self.screen_step_edit.ids.times_entry.text.isnumeric() == False:
            self.screen_step_edit.ids.times_entry.error = True
            
            return 

            
    def step_save(self,step):
        
        self.step_int_type_check()
        
        if (self.screen_step_edit.ids.start_entry.error == False and 
            self.screen_step_edit.ids.often_entry.error == False and 
            self.screen_step_edit.ids.times_entry.error == False):
            
            step['Code'] = self.screen_step_edit.ids.code_entry.text
            step['Action'] = self.screen_step_edit.ids.action_entry.text
            step['StartRow'] = int(self.screen_step_edit.ids.start_entry.text)
            step['HowManyTimes'] = int(self.screen_step_edit.ids.times_entry.text)
            step['HowOften'] = int(self.screen_step_edit.ids.often_entry.text)
            step['FontColor'] = self.screen_step_edit.ids.font_entry.text
            
            self.write_projects()  
            self.step_exit()


    def step_exit(self):
        '''
        exit the step edit menu back to the piece listing
        '''
        
        self.piece_build(self.wk_piece_name)

        
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
        
        self.set_screen(self.ListScreenName)

        self.screen_name = self.RootScreenName
        
        self.menu_build(self.root_menu_labels)
        
        self.list_build(self.projects.keys())

        
    def root_menu_callback(self, text_item):
        Snackbar(text=text_item).open()

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
        self.set_screen(self.ListScreenName)

        self.screen_name = self.ProjectScreenName
        
        # set variables for the selected working project
        self.wk_project_vars(project_name)

        # update the toolbar title and menu items
        # self.root.toolbar.title = self.wk_project_name
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
        
            self.set_screen(self.TableScreenName)
            self.wk_piece_vars(piece_name)
            self.menu_build(self.piece_menu_labels) 
            
            self.wk_piece = self.wk_project['Pieces'][piece_name]
            # self.wk_piece_name = 
            self.steps_table_build(self.wk_piece)
            # self.steps_steps_table_build()
            # Snackbar(text=piece_name).open()



# =============================================================================
# build application
# =============================================================================
    def build(self):
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        self.set_vars()        
        self.read_projects()
        
        # set root to main app screen        
        self.root = AppScreen()
        self.root.ids.sm.transition = NoTransition()
        
        # create variables to access ids on each page
        self.screen_list = self.root.ids.sm.get_screen(self.ListScreenName)
        self.screen_table = self.root.ids.sm.get_screen(self.TableScreenName)
        self.screen_step_edit = self.root.ids.sm.get_screen(self.StepEditScreenName)
        # build the main page
        self.root_build()


        return self.root


if __name__ == '__main__':
    MainApp().run()