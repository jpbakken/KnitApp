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
# from kivymd.uix.scrollview import ScrollView

# froxm kivymd.uix.scrollview import MDScrollView
# from kivymd.uix.boxlayout import BoxLayout
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.button import MDRaisedButton
# from kivy.uix.settings import Settings
# import pandas as pd
# from kivymd.uix.tab import MDTabsBase

class RootWidget(MDFloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.
    Add an action to be called from a kv file.
    '''

    container = ObjectProperty(None)

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
    def set_vars(self):
        """
        Define variables that can be used throughout
        """
        self.project_menu_labels = ['Add Piece',
                                    'Back to Projects',
                                    'Clear Box Widget',
                                    'Settings']
        
        self.root_menu_labels = ['New Project',
                                    'Clear Box Widget',
                                 'Settings']
        
        self.toolbar_title = 'Projects'


    def menu_open(self, button):
        self.menu.caller = button
        self.menu.open()


    def menu_callback(self, text_item):
        self.menu.dismiss()
        
        if text_item == 'Settings':
            self.open_settings()
        
        elif text_item == 'Clear Box Widget':
            self.widget_hide(self.screen.ids.list)
            
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
        self.screen.toolbar.left_action_items = [
            ["menu", lambda x: self.menu_open(x)]]
        
        # set the toolbar title
        self.screen.toolbar.title = self.toolbar_title
    

# =============================================================================
# gui build - list of items in scrollview
# =============================================================================
    def list_build(self,items):
        '''
        clear and build the items to display in self.screen.ids.list
        '''
        
        # show the empty scroll list
        self.widget_visible(self.screen.ids.list)

        # iterate through items and build the scroll list
        for i in items:
            self.screen.ids.list.add_widget(
                OneLineListItem(
                    text="{}".format(i),
                    on_release=lambda x=i: self.list_on_release(x.text),))
            
            
    def list_on_release(self, text_item):
        '''
        what to do when an item in the list object is released
        
        self.screen_name is set in the _build functions for each screen
        '''
        
        if self.screen_name == 'root':
            self.project_build(text_item)
            
        elif self.screen_name == 'project':
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
        
        self.screen_name = 'root'
        
        self.menu_build(self.root_menu_labels)
        
        self.list_build(self.projects.keys())


    def root_rebuild(self):
        # self.screen.toolbar.title =  self.toolbar_title
        self.root_build()
        
    def root_menu_callback(self, text_item):
        Snackbar(text=text_item).open()

# =============================================================================
# gui build - project page
# =============================================================================

    def project_build(self, project_name):
        '''
        build the working project screen
            -- set toolbar title and menu items
            -- build scroll list and fill with pieces
            
        self.screen_name is used in functions that determine 
            what happens when list item and menus are clicked 

        '''
        self.screen_name = 'project'
        
        # set variables for the selected working project
        self.wk_project_vars(project_name)

        # update the toolbar title and menu items
        # self.screen.toolbar.title = self.wk_project_name
        self.menu_build(self.project_menu_labels)            

        # rebuild self.screen.ids.list
        self.list_build(self.wk_pieces)
        
        
    def project_menu_callback(self, text_item):
        
        if text_item == 'Back to Projects':
            self.root_rebuild()

        else:
            Snackbar(text=text_item).open()
            
            
            
        
    def piece_build(self, piece_name):
        
            Snackbar(text=piece_name).open()
        
    # def project_build(self):
        
    #     for i in self.wk_piece:
    #         self.screen.ids.list.add_widget(
    #             OneLineListItem(text="{0}: {1}".format(i['Code'],
    #                                                   i['Action']))
    #         )
        
    def project_menu_right_open(self, button):
        self.dots.caller = button
        self.dots.open()


    def project_menu_right_callback(self, text_item):
        self.dots.dismiss()
        Snackbar(text=text_item).open()

        
    def project_menu_right_build(self):
        
        menu_labels = ['Edit Project',
                        'Jump to row',
                        'Restart Project',
                        ]
        
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "height": dp(56),
                "on_release": lambda x=i: self.menu_right_callback(x),
              } for i in menu_labels
        ]
        
        self.dots = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

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
        self.root.add_widget(self.data_tables)
        




# =============================================================================
# build application
# =============================================================================
    def build(self):
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        
        self.read_projects()
        
        # # selection of work project
        # wk_project_name = 'Redford Sweater Size 2'
        # self.wk_project = self.projects[wk_project_name]   
        
        # wk_piece_name = 'Side Panel'
        # self.wk_piece = self.wk_project['Pieces'][wk_piece_name]
        
        self.set_vars()
        
        self.screen = Builder.load_file('kv/root.kv')

        self.root_build()


        return self.screen


if __name__ == '__main__':
    MainApp().run()