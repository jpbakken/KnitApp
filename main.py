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
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import MDDataTable
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import NoTransition


# from kivymd.uix.scrollview import ScrollView

# froxm kivymd.uix.scrollview import MDScrollView
# from kivymd.uix.boxlayout import BoxLayout
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.button import MDRaisedButton
# from kivy.uix.settings import Settings
# import pandas as pd
# from kivymd.uix.tab import MDTabsBase
Builder.load_file('kv/root.kv')

class AppScreen(Screen):
    pass

class ListScreen(Screen):
    pass

class TableScreen(Screen):
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

            self.steps_table_build()
            # Snackbar(text=piece_name).open()
    

    def steps_table_build(self):
        
        table_rows = []
        for step in self.wk_piece:
            table_rows.append(
                (step['Code'],
                 step['Action'],
                 step['HowManyTimes'],
                 step['HowOften'],
                 step['StartRow'],
                 step['FontColor'],
                 step['NumRows'],
                 step['EndOnRow'],)
                )
           
        self.data_tables = MDDataTable(
            # id='datatable',
            size_hint=(0.7, 0.6),
            use_pagination=True,
            check=True,
            # name column, width column, sorting function column(optional)
            column_data=[
                ("Code", dp(40)),
                ("Action", dp(100)),
                ("How Many Times", dp(20)),
                ("How Often", dp(20)),
                ("Start Row", dp(20)),
                ("Font Color", dp(20)),
                ("Num Rows", dp(20)),
                ("End on Row", dp(20)),
            ],
            row_data = table_rows
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)

        self.screen_table.ids.box.clear_widgets()
        self.screen_table.ids.box.add_widget(self.data_tables)
        


    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        # Snackbar(text=instance_row).open()
        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''
        # Snackbar(text=current_row).open()

        print(instance_table, current_row)




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

        # build the main page
        self.root_build()


        return self.root


if __name__ == '__main__':
    MainApp().run()