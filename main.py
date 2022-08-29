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
from typing import Union
import os

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.pickers import MDColorPicker
from kivy.uix.settings import SettingsWithTabbedPanel

from kivymd.uix.snackbar import Snackbar
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from itertools import compress
import kv

# from kivy.uix.label import Label
# from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout

class EditProjectPopup(MDBoxLayout):
    pass


class MainApp(MDApp):
    use_kivy_settings = False
    color_picker = None
    edit_project_dialog = None


# =============================================================================
# settings page
# =============================================================================
    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('App Settings', {'style': 'Dark', 
                                            'palette': 'Gray',
                                            'hue': '500'})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.add_json_panel('App Settings', self.config, data=kv.settings_json)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """

        if section == 'App Settings':
            if key == "style":
                self.theme_cls.theme_style = value
            elif key == 'palette':
                self.theme_cls.primary_palette = value
            elif key == 'hue':
                self.theme_cls.primary_hue = value


    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        super(MainApp, self).close_settings(settings)

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

    def write_substeps(self,piece_name):
        '''
        '''
        self.wk_substeps_dir = '{0}/{1}/Substeps'.format(self.data_dir,
                                                         self.wk_project_name)
        
        self.wk_substeps_file = '{}.json'.format(piece_name)
        self.wk_substeps_path = os.path.join(self.wk_substeps_dir,
                                             self.wk_substeps_file)

        # create the path if it doesn't exist
        if not os.path.exists(self.wk_substeps_dir):
            os.makedirs(self.wk_substeps_dir)
            
        with open(self.wk_substeps_path, 'w') as f:
            json.dump(self.wk_substeps, f)
            
        self.read_projects()

    def read_projects(self):
        try:
            with open(self.data_dir + '/projects.json', 'r') as json_file:     
                  self.projects = json.load(json_file)
                  # print(self.projects)
        except:
            with open('data/projects.json', 'r') as json_file:     
                  self.projects = json.load(json_file)
             
    def wk_project_vars(self,project_name):
        '''
        set working project variables
        '''        
        self.toolbar_title = project_name        
        self.screen_name = self.ProjectScreenName

        self.wk_project = self.projects[project_name]
        self.wk_project_name = project_name

        self.wk_pieces = self.wk_project['Pieces'].keys()

        
    def wk_piece_vars(self,piece_name,selected_piece_idx = 0):
        '''
        '''
        self.toolbar_title = self.wk_project_name + ': ' + piece_name
        self.screen_name = self.PieceScreenName

        self.wk_piece_name = piece_name
        self.wk_piece = self.wk_project['Pieces'][piece_name]
        
        self.wk_step = self.wk_piece[selected_piece_idx]


# =============================================================================
# class variables
# =============================================================================

    def set_vars_layout(self):
        '''
        define variables that are used in layouts
        '''
        self.settings_cls = SettingsWithTabbedPanel

        self.theme_cls.theme_style = self.config.get(self.app_settings_label,
                                                     'style')
        self.theme_cls.primary_palette = self.config.get(self.app_settings_label,
                                                     'palette')
        self.theme_cls.primary_hue = self.config.get(self.app_settings_label,
                                                     'hue')


        self.root= Builder.load_string(kv.main_screen)
        self.step_edit_layout = Builder.load_string(kv.step_edit_screen)

    def set_vars(self):
        """
        Define variables that can be used throughout
        """
        self.set_data_dir()
        
        self.app_settings_label = 'App Settings'

        self.menu_item_settings = 'Settings'

        self.root_menu_create_project = 'Create New Project'
        # self.root_menu_item_2 = 'root_menu_item_2'

        self.root_menu_labels = [self.root_menu_create_project,
                                 # self.root_menu_item_2,
                                  self.menu_item_settings
                                  ]

        self.project_menu_add_piece = 'Add New Piece'
        self.project_menu_edit_name = 'Edit Project Name'
        self.project_menu_back_to_root = 'Back to Projects'
        
        
        self.project_menu_labels = [self.project_menu_add_piece,
                                    self.project_menu_edit_name,
                                    self.project_menu_back_to_root,
                                    # self.menu_item_settings,
                                    ]

        self.piece_menu_add_step = 'Add New Step'
        self.piece_menu_edit_name = 'Edit Piece Name'
        self.piece_menu_back_to_project = 'Back to Project Pieces'
        
        self.piece_menu_labels = [self.piece_menu_add_step,
                                  self.piece_menu_edit_name,
                                  self.piece_menu_back_to_project,
                                  # self.menu_item_settings,
                                  ]
        
        
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
        '''
        '''
        widget.disabled = True
        widget.opacity = 0
        widget.clear_widgets()
        
    def widget_visible(self,widget):
        '''
        '''
        widget.clear_widgets()
        widget.disabled = False
        widget.opacity = 1
        
    def clear_layout(self):
        '''
        '''
        self.widget_visible(self.root.ids.header)
        self.root.ids.header.text = ''
        self.widget_visible(self.root.ids.content_col)
        self.widget_visible(self.root.ids.content_main)

        

# =============================================================================
# gui build - menu
# =============================================================================
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


    def menu_open(self, button):
        '''
        '''
        self.menu.caller = button
        self.menu.open()


    def menu_callback(self, text_item):
        '''
        '''
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


    def root_menu_callback(self, text_item):
        '''
        '''
        if text_item == self.root_menu_create_project:
            Snackbar(text=text_item).open()
            
        else:
            Snackbar(text=text_item).open()
        

    def project_menu_callback(self, text_item):
        '''
        '''
        
        if text_item == self.project_menu_add_piece:
            Snackbar(text=text_item).open()
        
        elif text_item == self.project_menu_edit_name:
            self.project_name_edit_dialog()
            #TODO: changing name requires changing other things/files?
            # project name unique test, similar to step_code_unique_check
            
            Snackbar(text=text_item).open()

        elif text_item == self.project_menu_back_to_root:
            self.root_build()

        else:
            Snackbar(text=text_item).open()
    

    def piece_menu_callback(self, text_item):
        '''
        '''

        if text_item == self.piece_menu_add_step:
            Snackbar(text=text_item).open()
             
        elif text_item == self.piece_menu_edit_name:
            #TODO: changing name requires changing other things?
            # piece name unique check, similar to step_code_unique_check 

            Snackbar(text=text_item).open()
             
        elif text_item == self.piece_menu_back_to_project:
            
            self.step_save()
            
            if self.validation_error == False:
                self.project_build(self.wk_project_name)
            
        else:
            Snackbar(text=text_item).open()


# =============================================================================
# gui build - list of items in scrollview
# =============================================================================

    def item_list_build(self, items, widget):
        '''
        build a clickable scroll list of test items
        
        Input:
            a list of text items
        Action:
            self.item_list_on_release('item text')
        '''
        
        # show an empty content area
        self.widget_visible(self.root.ids.content_main)
        
        # create list and add the items
        mdlist = MDList()        

        # iterate through items and build the scroll list
        for i in items:
            mdlist.add_widget(
                OneLineListItem(
                    text="{}".format(i),
                    on_release=lambda x=i: self.item_on_release(x.text),))
                        
        # add list to the scroll view
        scroll = ScrollView()
        scroll.add_widget(mdlist)

        # add widget to the content area
        widget.add_widget(scroll)


    def item_on_release(self, text_item):
        '''
        what to do when an item in the list object is released
        
        self.screen_name is set in the _build functions for screens
        '''
        
        if self.screen_name == self.RootScreenName:
            self.project_build(text_item)
            
        elif self.screen_name == self.ProjectScreenName:
            self.piece_steps_edit_build(text_item)
        
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
        
        self.clear_layout()


        self.read_projects()
        
        self.menu_build(self.root_menu_labels)
        
        self.item_list_build(self.projects.keys(),
                             self.root.ids.content_main)


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
        
        # show and clear anything left in the main layout
        self.clear_layout()

        # set variables for the selected working project
        self.wk_project_vars(project_name)

        # update the toolbar title and menu items
        self.menu_build(self.project_menu_labels)            

        self.root.ids.header.text = 'Select a step to edit'
        
        # build the list of pieces
        self.item_list_build(self.wk_pieces,
                             self.root.ids.content_main)
        
        # build the edit pieces buttons
        self.project_pieces_buttons_build()
        

    def project_name_edit_dialog(self):
        if not self.edit_project_dialog:
            self.edit_project_dialog = MDDialog(
                title="Enter new project name:",
                type="custom",
                pos_hint = {'center_x': .5, 'top': .9},
                content_cls=EditProjectPopup(),
                buttons=[
                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.project_name_edit_dismiss),
                    MDFlatButton(
                        text="Save",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        # on_release= ,
                        )
                    ]
                )
            
        self.edit_project_dialog.open()
        
    def project_name_edit_dismiss(self, inst):
        self.edit_project_dialog.dismiss()

    def project_pieces_buttons_build(self):
        '''
        '''
        # show and clear anything left in the widget
        self.widget_visible(self.root.ids.content_col)

        # create list and add the items
        mdlist = MDList()
        column_header = 'Knit a step'
        mdlist.add_widget(
            OneLineListItem(
                text=column_header,
                disabled=True,
                ))

        for piece in self.wk_pieces:
                        
            button = MDRaisedButton(
                        text=piece,
                        size_hint = (1,.8),
                        on_release = lambda x=piece: self.knit_piece(x.text),
                        )
                    
            mdlist.add_widget(button)
                    
        # add list to the scroll view
        scroll = ScrollView()
        scroll.add_widget(mdlist)
        
        self.root.ids.content_col.add_widget(scroll)

    def calc_substeps(self,piece_name):
        '''
        '''
               
        self.wk_substeps = []
        wk_piece = self.wk_project['Pieces'][piece_name]

        
        for idx, step in enumerate(wk_piece):
            StepRow = step['StartRow']
            HowOften = step['HowOften']
            HowManyTimes = step['HowManyTimes']
            Code = step['Code']
            Action = step['Action']
            FontColor = step['FontColor']
            
            for substep in range(HowManyTimes):
                self.wk_substeps.append({'Step Row': StepRow,
                                 'Code': Code,
                                 'Action': Action,
                                 'FontColor': FontColor})
                
                # increment to next row to add
                StepRow =  StepRow + HowOften

        self.write_substeps(piece_name)

 # def wk_substeps_vars(self,piece_name):
     
     # self.wk_substeps = []
     # self.wk_project['Substeps'][piece_name] = []
     # try:
     #     self.wk_substeps = self.wk_project['Substeps'][piece_name]
         
     # except KeyError:
     #     self.wk_project['Substeps'][piece_name] = []
     #     self.wk_substeps = self.wk_project['Substeps'][piece_name]


    def get_current_substeps(self,step_row):
        
        current_substeps = [
            sub['Step Row'] == step_row for sub in self.wk_substeps]
        
        self.step_row_substeps = list(compress(self.wk_substeps,
                                     current_substeps))
        
#TODO: save progress for project/step

    def knit_piece(self, piece_name):
        '''
        '''
        #TODO: if work in progress then calc substeps
        self.calc_substeps(piece_name)
        #TODO: else read substeps and set working row
        
        #TODO: open work substeps screen
        #button to move forward row
        #button to move back row
        #button to jump to step

        
        

# =============================================================================
# gui build - piece page (listing steps)    
# =============================================================================
    def piece_steps_edit_build(self, piece_name):
        '''
        '''
        
        # set variables for the selected working piece
        self.wk_piece_vars(piece_name)
        
        # update the toolbar title and menu items
        self.menu_build(self.piece_menu_labels) 
        
        # show and clear anything left in the widget
        self.clear_layout()
                
        # build the code buttons and edit screen
        self.steps_code_buttons_build()
        self.step_edit_fields_build()
        

    def steps_code_buttons_build(self):
                
        # show and clear anything left in the widget
        self.widget_visible(self.root.ids.content_col)

        # create list and add the items
        mdlist = MDList()     
        
        for piece in self.wk_piece:
            
            # print(piece['FontColor'])
            
            code = piece['Code']
            
            button = MDRaisedButton(
                        text=code,
                        size_hint = (1,.8),
                        on_release = lambda x=code: self.step_edit(x.text),
                        md_bg_color = piece['FontColor'],
                        )
                    
            mdlist.add_widget(button)
                    
        # add list to the scroll view
        scroll = ScrollView()
        scroll.add_widget(mdlist)
        
        self.root.ids.content_col.add_widget(scroll)
        
       
    def step_edit(self,step_code):
        '''
        screen to edit or delete a step
        '''        
        # save the values of the current step before switching
        self.step_save()
        
        if self.validation_error == False:
            self.step_set_text(step_code)
            
        
    def step_edit_fields_build(self):
        '''
        '''
        # show and clear anything left in the widget
        self.widget_visible(self.root.ids.content_main)
        
        # set the header and content layout and 
        self.root.ids.content_main.add_widget(self.step_edit_layout)     

        self.step_set_text(self.wk_step['Code'])        


    def step_get_work_dict(self,step_code):
        '''
        '''
        # get the dict values for the selected step
        try:
            wk_step_idx = next(
                (index for (index, d) in enumerate(
                    self.wk_piece) if d["Code"] == step_code), -1)
        except:
            wk_step_idx = -1
        
        return wk_step_idx


    def step_set_text(self, step_code):
        '''
        set peice to saved values
        '''
        # set variable with the index of the current step
        self.wk_step_idx = self.step_get_work_dict(step_code)
        
        # set variable with the working step dictionary items
        self.wk_step = self.wk_piece[self.wk_step_idx]
        step = self.wk_step
        
        self.step_edit_layout.ids.code_entry.text = step['Code']
        self.step_edit_layout.ids.action_entry.text = step['Action']
        self.step_edit_layout.ids.start_entry.text = str(step['StartRow'])
        self.step_edit_layout.ids.times_entry.text = str(step['HowManyTimes'])
        self.step_edit_layout.ids.often_entry.text = str(step['HowOften'])
        
        # self.step_edit_layout.ids.font_entry.md_bg_color = step['FontColor']
        self.root.ids.header.text = 'Edit piece: ' + step['Code']


    def step_int_type_check(self):
        '''
        check to make sure number fields from the edit text screen are numeric
        '''

        if self.step_edit_layout.ids.start_entry.text.isnumeric() == False:
            self.step_edit_layout.ids.start_entry.error = True
            self.validation_error = True
        if self.step_edit_layout.ids.often_entry.text.isnumeric() == False:
            self.step_edit_layout.ids.often_entry.error = True
            self.validation_error = True
        if self.step_edit_layout.ids.times_entry.text.isnumeric() == False:
            self.step_edit_layout.ids.times_entry.error = True
            self.validation_error = True


    def step_code_unique_check(self):
        '''
        Checks to make sure the step code is unique
        '''
        step_code = self.step_edit_layout.ids.code_entry.text
        
        if (self.step_get_work_dict(step_code) > -1 and 
            self.step_get_work_dict(step_code) != self.wk_step_idx):
            
            self.step_edit_layout.ids.code_entry.error = True
            self.validation_error = True
        
        
    def step_save(self):
        '''
        '''
        step = self.wk_step
        
        self.validation_error = False

        self.step_int_type_check()
        self.step_code_unique_check()
        
        if self.validation_error == False:
            
            step['Code'] = self.step_edit_layout.ids.code_entry.text
            step['Action'] = self.step_edit_layout.ids.action_entry.text
            step['StartRow'] = int(self.step_edit_layout.ids.start_entry.text)
            step['HowManyTimes'] = int(self.step_edit_layout.ids.times_entry.text)
            step['HowOften'] = int(self.step_edit_layout.ids.often_entry.text)
            
            # update the piece with step values and write the changes
            self.wk_piece[self.wk_step_idx] = step
            
            self.wk_project['Pieces'][self.wk_piece_name][self.wk_step_idx] = step
            
            self.write_projects()  
            
            self.wk_project_vars(self.wk_project_name)
            self.wk_piece_vars(self.wk_piece_name, self.wk_step_idx)
            
            # update the buttons
            self.steps_code_buttons_build()
            
    
    def open_color_picker(self):
        '''
        '''
        self.color_picker = MDColorPicker(
            size_hint=(0.45, 0.85),
            default_color=self.wk_step['FontColor'],
            
            )
        self.color_picker.open()
        self.color_picker.bind(
            on_select_color=self.on_select_color,
            on_release=self.get_selected_color,
        )


    def update_color(self, color: list) -> None:
        '''
        '''
        self.wk_step['FontColor'] = color
        # self.step_edit_layout.ids.font_entry.md_bg_color = color
        self.step_save()


    def get_selected_color(self,
                           instance_color_picker: MDColorPicker,
                           type_color: str,
                           selected_color: Union[list, str]):
        '''
        '''
        self.update_color(selected_color[:-1] + [1])
        self.color_picker.dismiss()


    def color_picker_dismiss(self,inst):
        '''
        '''
        self.color_picker.dismiss()

    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''
        Called when a gradient image is clicked.
        '''

        
# =============================================================================
# build application
# =============================================================================
    def build(self):
        '''
        '''
        self.set_vars()   
        self.set_vars_layout()
        self.root_build()
        


if __name__ == '__main__':
    MainApp().run()