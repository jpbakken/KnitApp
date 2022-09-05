#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: jpbakken
"""
import kv
import dropbox
from itertools import compress
import json
import os
import shutil
from typing import Union
import zipfile

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.uix.settings import SettingItem
from kivy.uix.scrollview import ScrollView
import kivy.utils as utils

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import MDList
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDColorPicker
from kivymd.uix.snackbar import Snackbar





class EditFieldDialog(MDBoxLayout):
    pass

class ColorPickerDialog(MDBoxLayout):
    pass

class SettingButtons(SettingItem):

    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        # For Python3 compatibility we need to drop the buttons keyword when calling super.
        kw = kwargs.copy()
        kw.pop('buttons', None)
        super(SettingItem, self).__init__(**kw)
        for aButton in kwargs["buttons"]:
            oButton=MDRaisedButton(text=aButton['title'], font_size= '15sp')
            oButton.ID=aButton['id']
            self.add_widget(oButton)
            oButton.bind (on_release=self.On_ButtonPressed)
            
            
    def set_value(self, section, key, value):
        # set_value normally reads the configparser values and runs on an error
        # to do nothing here
        return
    
    def On_ButtonPressed(self,instance):
        self.panel.settings.dispatch('on_config_change',
                                     self.panel.config, 
                                     self.section, 
                                     self.key, 
                                     instance.ID)


class KnitApp(MDApp):
# =============================================================================
# initialize empty dialog variables
# =============================================================================
    use_kivy_settings = False
    color_picker = None
    edit_field_dialog = None
    knit_piece_complete = None

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
        '''
        set the data directory to the user data directory for the app
        
        copy sample files from app data directory if user directory is empty
        '''
        app = MDApp.get_running_app()
        self.data_dir = app.user_data_dir
        self.copy_data_dir()


    def copy_data_dir(self):
        '''
        if self.data_dir is empty, copy the sample data dir
        '''
        target_dir = self.data_dir
        source_dir = 'data'
        
        #if target directory has no project folders 
        if not [d for d in next(os.walk(target_dir))[1]]:
            # get list of files from the source directory
            files=os.listdir(source_dir)
            
            # copy files and directories from source to target
            for file in files:                
                src = os.path.join(source_dir,file)
                tgt = os.path.join(target_dir,file)
                
                if os.path.isdir(src):
                    shutil.copytree(src, tgt)
                else:
                    shutil.copy2(src, target_dir)

    
    def get_project_list(self):
        '''
        get and sort project list from the app data directory
        '''
        self.project_list = [d for d in next(os.walk(self.data_dir))[1] \
                             if d != '_backups']
        self.project_list.sort()
        
        
    def get_wk_pieces_list(self):
        '''
        get and sort pieces list from the working project directory
        '''
        self.wk_pieces_list = os.listdir(self.wk_pieces_dir)
        self.wk_pieces_list = [name.split('.')[0] for name in self.wk_pieces_list]


    def get_wk_in_progress(self):
        '''
        get work in progress for a piece, or create one if there is not one
        '''
        
        if os.path.exists(self.wk_in_progress_filename):
            with open(self.wk_in_progress_filename) as json_file:     
                 self.wk_piece_in_progress = json.load(json_file)

        else:
            self.wk_piece_in_progress = self.new_wk_in_progress
            
        self.knit_step_row = self.wk_piece_in_progress['StepRow'] 


    def get_wk_substeps(self):
        '''
        get substeps list from the working project directory
        '''
        self.get_wk_in_progress()
        
        if (self.wk_piece_in_progress['StepRow'] > 1 and 
            os.path.exists(self.wk_substeps_filename)):
            
                with open(self.wk_substeps_filename) as json_file:     
                     self.wk_substeps = json.load(json_file)
                     
        else:
            self.calc_substeps()


    def write_wk_piece(self):
        '''
        write a json file for the working piece dictionary
        '''
        self.wk_piece.sort(key=self.sort_steps)

        with open(self.wk_piece_filename, 'w') as f:
            json.dump(self.wk_piece, f)
               
            
    def write_wk_step_in_progress(self):
        '''
        '''
        self.wk_piece_in_progress['StepRow'] = self.knit_step_row
                
        with open(self.wk_in_progress_filename, 'w') as f:
            json.dump(self.wk_piece_in_progress, f)


    def write_wk_substeps(self):
        '''
        write a json file for the working substeps dictionary
        '''
        with open(self.wk_substeps_filename, 'w') as f:
            json.dump(self.wk_substeps, f)
            
        
        self.write_wk_step_in_progress()
            
        
    def read_piece(self):
        '''
        '''
        with open(self.wk_piece_filename, 'r') as json_file:     
              self.wk_piece = json.load(json_file)
        
    
    def sort_steps(self, e):
        return e['StartRow']
              

# =============================================================================
# variables that get set when objects are selected (projects, pieces, etc)        
# =============================================================================
    def set_project_vars(self,project_name):
        '''
        set working project variables
        '''        
        self.toolbar_title = project_name       
        
        self.wk_project_name = project_name

        self.wk_project_data_dir = os.path.join(self.data_dir,
                                                self.wk_project_name)
        
        self.wk_pieces_dir = os.path.join(self.wk_project_data_dir,
                                          'Pieces')
     
        self.wk_substeps_dir = os.path.join(self.wk_project_data_dir,
                                            'Substeps')

        self.wk_in_progress_dir = os.path.join(self.wk_project_data_dir,
                                               'WorkInProgress')

        self.get_wk_pieces_list()        

        self.edit_field_name = 'Edit Project Name'
        self.edit_field_text = self.wk_project_name
        self.edit_field_check_list = self.project_list

        
    def set_piece_vars(self,piece_name,selected_piece_idx = 0):
        '''
        set working piece variables
        '''
        self.wk_piece_name = piece_name

        self.toolbar_title = self.wk_project_name + ': ' + self.wk_piece_name
        

        # set menu labels fpr on_release of a list item
        self.list_menu_labels = self.list_menu_labels_piece
        
        self.set_piece_filenames()

        # read the piece file
        self.read_piece()
        
        # set variable for the selected step or the first step
        self.wk_step = self.wk_piece[selected_piece_idx]
        
        self.edit_field_name = 'Edit Piece Name'
        self.edit_field_text = piece_name
        self.edit_field_check_list = self.wk_pieces_list

    
    def set_piece_filenames(self):
        '''
        set filenames for project pieces and substeps
        '''
        
        dirs = [self.wk_pieces_dir,
                self.wk_substeps_dir,
                self.wk_in_progress_dir]
        
        for d in dirs:
            # create the path if it doesn't exist
            if not os.path.exists(d):
                os.makedirs(d)

        self.wk_piece_filename = os.path.join(self.wk_pieces_dir, 
                                   self.wk_piece_name + '.json')
        
        self.wk_substeps_filename = os.path.join(self.wk_substeps_dir, 
                                   self.wk_piece_name + '.json')

        self.wk_in_progress_filename = os.path.join(self.wk_in_progress_dir, 
                                                    self.wk_piece_name \
                                                        + '.json')


# =============================================================================
# class variables
# =============================================================================
    def set_app_vars(self):
        """
        Define variables that can be used throughout
        """

        self.set_data_dir()

        # define custom settings options
        self.set_settings_vars()

        # get the list of saved projects
        self.get_project_list()

        # import the layout strings
        self.root= Builder.load_string(kv.main_screen)
        self.step_edit_layout = Builder.load_string(kv.step_edit_screen)

        # set name of the settings menu item
        self.menu_item_settings = 'Settings'

        # set names for the root toolbar menu
        self.root_menu_create_project = 'Create New Project'
        
        self.root_menu_labels = [self.root_menu_create_project,
                                 self.menu_item_settings]


        # project toolbar menu
        self.project_menu_add_piece = 'Add New Piece'
        self.project_menu_edit_name = 'Edit Project Name'
        self.project_menu_back_to_root = 'Back to Projects'
        self.project_menu_project_backup = 'Backup Project'
        
        
        self.project_menu_labels = [self.project_menu_add_piece,
                                    self.project_menu_edit_name,
                                    self.project_menu_back_to_root,
                                    self.project_menu_project_backup,
                                    ]
        
        # piece select list menu
        self.piece_menu_knit = 'Knit Piece'
        self.piece_menu_edit_steps = 'Edit Piece'
        
        self.list_menu_labels_piece = [self.piece_menu_knit,
                                       self.piece_menu_edit_steps,]

        # piece page toolbar menu
        self.piece_menu_add_step = 'Add New Step'
        self.piece_menu_delete_step = 'Delete Selected Step'
        self.piece_menu_back_to_project = 'Back to Project Pieces'
        self.piece_menu_edit_name = 'Edit Piece Name'
        
        self.piece_menu_labels = [self.piece_menu_add_step,
                                  self.piece_menu_delete_step,
                                  self.piece_menu_knit,
                                  self.piece_menu_edit_name,
                                  self.piece_menu_back_to_project,]
        
        
        self.piece_knit_menu_reset = 'Reset progress'

        self.piece_knit_menu_labels = [self.piece_knit_menu_reset,
                                       self.piece_menu_back_to_project,
                                       ]
        
        self.piece_knit_button_previous = 'Previous Step'
        self.piece_knit_button_jump = 'Jump to Step'
        self.piece_knit_button_next = 'Next Step'
        
        self.piece_knit_button_labels = [self.piece_knit_button_previous,
                                         self.piece_knit_button_jump,
                                         self.piece_knit_button_next]

        
        self.new_step_dict = {"StepRow": 1,
                              "Action": "",
                              "HowManyTimes": 1, 
                              "HowOften": 1, 
                              "StartRow": 1, 
                              "FontColor": self.color_select1
                              }

        self.new_wk_in_progress = {"StepRow": 1}


        self.toolbar_title = 'Projects'
        
        self.StepEditScreenName = 'stepedit'
        
        self.RootScreenName = 'root'
        self.ProjectScreenName = 'project'
        self.PieceScreenName = 'piece'
        self.PieceKnitScreenName = 'knit'

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
# gui build - toolbar menu
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


    def menu_open(self, instance):
        '''
        '''
        self.menu.caller = instance
        self.menu.open()


    def menu_callback(self, menu_item):
        '''
        main menu callback. calls page-specific menu items
            or items that can be found on multiple pages
        '''
        self.menu.dismiss()
        
        if menu_item == 'Settings':
            self.open_settings()
                                
        elif self.screen_name == self.RootScreenName:
            self.root_menu_callback(menu_item)

        elif self.screen_name == self.ProjectScreenName:
            self.project_menu_callback(menu_item)

        elif self.screen_name in [self.PieceScreenName,
                                  self.PieceKnitScreenName]:
            self.piece_menu_callback(menu_item)


    def root_menu_callback(self, menu_item):
        '''
        '''
        if menu_item == self.root_menu_create_project:
            self.create_project()


    def project_menu_callback(self, menu_item):
        '''
        '''
        if menu_item == self.project_menu_add_piece:
            self.create_piece()
            
        elif menu_item == self.project_menu_edit_name:
            self.dialog_field_build()

        elif menu_item == self.project_menu_back_to_root:
            self.root_build()
            
        elif menu_item == self.project_menu_project_backup:
            self.project_backup()
    

    def piece_menu_callback(self, menu_item):
        '''
        '''

        if menu_item == self.piece_menu_add_step:
            self.create_step()
            
        elif menu_item == self.piece_menu_delete_step:
            self.step_delete()
                
        elif menu_item == self.piece_menu_knit:
            self.knit_piece_build() 

        elif menu_item == self.piece_menu_edit_name:
            self.dialog_field_build()
        

        elif menu_item == self.piece_menu_back_to_project:
            
            if self.screen_name == self.PieceScreenName:
                self.step_save()
                
                if self.validation_error == False:
                    self.project_build(self.wk_project_name)
                    
            elif self.screen_name == self.PieceKnitScreenName:
                self.project_build(self.wk_project_name)

        elif menu_item == self.piece_knit_menu_reset:
            self.dialog_knit_piece_reset()

# =============================================================================
# gui build - list of items in scrollview
# =============================================================================

    def item_list_build(self, items, widget):
        '''
        build a clickable scroll list of test items
        
        Input:
            a list of text items
        Action:
            self.item_list_menu_on_release
        '''
        
        # show an empty content area
        self.widget_visible(widget)

        scroll = Builder.load_string(kv.scroll_list_widget)
        
        # iterate through items and build the scroll list
        for i in items:
            scroll.ids.mdlist.add_widget(
                OneLineListItem(
                    text="{}".format(i),
                    on_release=self.item_list_menu_on_release,
                    ))
                        
        # add widget to the content area
        widget.add_widget(scroll)


    def item_list_menu_callback(self, menu_item):
        '''
        '''
        self.list_menu.dismiss()
        
        if self.screen_name == self.ProjectScreenName:
            
            if menu_item == self.piece_menu_knit:
                self.knit_piece_build() 
                
            elif menu_item == self.piece_menu_edit_steps:
                self.piece_edit_build()
                
            elif menu_item == self.piece_menu_show_steps:
                self.piece_steps_table_build(self.wk_piece_name)    
            
        else:
            Snackbar(text=menu_item).open()


    def item_list_menu_on_release(self, instance):
        '''
        '''
        # if on the main screen, click through to the list of project pieces
        if self.screen_name == self.RootScreenName:
            self.set_project_vars(instance.text)
            self.project_build(self.wk_project_name)

        # if on the project pieces screen, build set menu options
        elif self.screen_name == self.ProjectScreenName:
            self.set_piece_vars(instance.text)
            
            menu_items = [
                {"viewclass": "OneLineListItem",
                 "text": i,
                 "height": dp(56),
                 "on_release": lambda x=i:  self.item_list_menu_callback(x),
                 } for i in self.list_menu_labels]
    
            self.list_menu = MDDropdownMenu(caller=instance,
                                            items=menu_items,
                                            width_mult=4)
            
            self.list_menu.open()


# =============================================================================
# edit field dialog box build
# =============================================================================
    def dialog_field_build(self):
        '''
        popup dialog used to edit a field (e.g., project name)
        '''
        self.edit_field_dialog = MDDialog(
            title=self.edit_field_name,
            type="custom",
            pos_hint = {'center_x': .5, 'top': .9},
            content_cls=EditFieldDialog(),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_field_dismiss),
                MDFlatButton(
                    text="Save",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_field_name_save)])
        
        self.edit_field_dialog.open()
        
        
    def dialog_field_dismiss(self, inst):
        '''
        dismiss the dialog box
        '''
        self.edit_field_dialog.dismiss()


    def dialog_field_name_save(self, inst):
        '''
        check to make sure name is unique then save if it is
        '''
        # set variables for shortcuts
        edit_field = self.edit_field_dialog.content_cls.ids.edit_field
        new_value = edit_field.text

        # check to make sure new name is not already used in projects
        if next((key for key in self.edit_field_check_list \
                 if key == new_value), None):
            edit_field.error = True
            
        else:
            # if creating or editing a project name
            if 'Project Name' in self.edit_field_name:
                edit_field.helper_text=\
                    'There can be only one...name must be unique'
                self.dialog_project_name_save(new_value)

            # if creating or editing a piece name
            elif 'Piece Name' in self.edit_field_name:
                self.dialog_piece_name_save(new_value)
                
            
            elif self.edit_field_name == self.piece_knit_button_jump:
                end_row = self.wk_piece_in_progress['EndRow']
                
                if new_value.isnumeric() == False:
                    edit_field.helper_text='Wait...that is not a number'
                    edit_field.error = True
                    
                elif int(new_value) > end_row:
                    edit_field.helper_text='Hold your horses...{0} has only {1} rows.' \
                        .format(self.wk_piece_name,end_row)
                    edit_field.error = True

                else:
                    self.dialog_piece_jump_save(new_value)
                    
                
    def dialog_project_name_save(self, new_value):
        '''
        '''
        self.edit_field_dialog.dismiss()
        
        self.wk_project_name = new_value
        
        new_path = os.path.join(self.data_dir,new_value)
        
        # rename the project folder if editing a project name
        if 'Edit' in self.edit_field_name:
            os.rename(self.wk_project_data_dir, new_path) 
            
        # create the project folder if creating a new project
        elif 'New' in self.edit_field_name:
            # create project directories
            if not os.path.exists(new_path):
                os.makedirs(new_path)
                
        # refresh the list of saved projects
        self.get_project_list()

        self.project_build(self.wk_project_name)
        
        
    def dialog_piece_name_save(self, new_value):
        '''
        '''
        self.edit_field_dialog.dismiss()
        
        self.wk_piece_name = new_value

        # rename the pieces files if editing a project name
        if 'Edit' in self.edit_field_name:
            
            old_substeps_filename = self.wk_substeps_filename
            old_piece_filename = self.wk_piece_filename
            old_in_progres_filename = self.wk_in_progress_filename
            
            self.set_piece_filenames()

            if os.path.exists(old_substeps_filename):
                os.rename(old_substeps_filename, 
                          self.wk_substeps_filename)
                
            if os.path.exists(old_piece_filename):
                os.rename(old_piece_filename, 
                          self.wk_piece_filename)
            
            if os.path.exists(old_in_progres_filename):
                os.rename(old_in_progres_filename, 
                          self.wk_in_progress_filename)
                
            self.piece_edit_build()

        # create pieces folders/file if creating a new piece
        elif 'New' in self.edit_field_name:
            
            # add the first step to the piece
            self.wk_piece = []
            
            self.create_step()
            
            
    def dialog_piece_jump_save(self,new_value):
        '''
        on the knit page, jump to a specific step
        '''
        self.edit_field_dialog.dismiss()
        
        self.knit_step_row = int(new_value)
        self.knit_piece_content_build()
        
        self.write_wk_step_in_progress()

            
    def create_project(self):
        '''
        use edit field dialog to create a new project
        '''
        self.edit_field_name = 'New Project Name'
        self.edit_field_check_list = self.project_list
        self.edit_field_text = ''
        self.dialog_field_build()

    def create_piece(self):
        '''
        use edit field dialog to create a new piece
        '''
        self.edit_field_name = 'New Piece Name'
        self.edit_field_check_list = self.wk_pieces_list
        self.edit_field_text = ''
        self.dialog_field_build()
        
        
    def create_step(self):
        '''
        '''
        step = self.new_step_dict.copy()
        step['Code'] = step['Code'] + str(len(self.wk_piece)+1)
        
        self.wk_piece.append(step)
        
        self.wk_step_idx = self.step_get_work_idx(step['Code'])

        self.set_piece_filenames()
        
        self.write_wk_piece()
        
        self.piece_edit_build()
        
        
    def piece_knit_jump_to_step(self):
        '''
        '''
        self.edit_field_name = self.piece_knit_button_jump
        self.edit_field_check_list = [0]
        self.edit_field_text = str(self.knit_step_row)

        self.dialog_field_build()


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
        
        self.menu_build(self.root_menu_labels)
        
        self.item_list_build(self.project_list,
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
        self.set_project_vars(project_name)
        self.screen_name = self.ProjectScreenName


        # update the toolbar title and menu items
        self.menu_build(self.project_menu_labels)            

        # self.root.ids.header.text = 'Select a step to edit'
        
        # build the list of pieces
        self.item_list_build(self.wk_pieces_list,
                             self.root.ids.content_main)
        
        # build the edit pieces buttons
        self.project_pieces_buttons_build()
        

    def project_pieces_buttons_build(self):
        '''
        build something in content_col on the pieces page
        '''
        # show and clear anything left in the widget
        self.widget_visible(self.root.ids.content_col)
        

# =============================================================================
# substep fuctions used while knitting
# =============================================================================
    def calc_substeps(self):
        '''
        '''
               
        self.wk_substeps = []
        
        for idx, step in enumerate(self.wk_piece):
            StepRow = step['StartRow']
            HowOften = step['HowOften']
            HowManyTimes = step['HowManyTimes']
            Code = step['Code']
            Action = step['Action']
            FontColor = step['FontColor']
            CodeStepNum = 1
            for substep in range(HowManyTimes):
                self.wk_substeps.append({'StepRow': StepRow,
                                 'Code': Code,
                                 'Action': Action,
                                 'FontColor': FontColor,
                                 'CodeStepNum': CodeStepNum,
                                 'HowManyTimes': HowManyTimes
                                 })
                
                # increment to next row to add
                StepRow =  StepRow + HowOften
                CodeStepNum += 1

        self.get_min_max_knit_row()
        
        self.write_wk_substeps()

    def get_min_max_knit_row(self):
        '''
        '''
        
        self.wk_piece_in_progress['StartRow'] = 999
        self.wk_piece_in_progress['EndRow'] = 0
        
        for step in self.wk_substeps:
            if step['StepRow'] < self.wk_piece_in_progress['StartRow']:
                self.wk_piece_in_progress['StartRow'] = step['StepRow']
            
            if step['StepRow'] > self.wk_piece_in_progress['EndRow']:
                self.wk_piece_in_progress['EndRow'] = step['StepRow']
           
                
        # start = [step['StepRow'] for step in steps if step['StepRow'] < start]
        # end = [step['StepRow'] for step in steps if step['StepRow'] > end]
        

    def get_current_substeps(self):
                
        current_substeps = [
            sub['StepRow'] == self.knit_step_row for sub in self.wk_substeps]
        
        self.step_row_substeps = list(compress(self.wk_substeps,
                                     current_substeps))


    def knit_piece_build(self):
        '''
        '''
        self.screen_name =  self.PieceKnitScreenName

        # show and clear anything left in the main layout
        self.clear_layout()
        
        self.menu_build(self.piece_knit_menu_labels) 

        # get or create work substeps and row
        self.get_wk_substeps()
        
        self.knit_piece_content_build()
        self.knit_piece_button_build()

        
    def knit_piece_content_build(self):
        
        self.widget_visible(self.root.ids.content_main)

        self.get_current_substeps()
        
        # build the list of pieces
        mdlist = MDList()        
        mdlist.add_widget(TwoLineListItem(disabled=True))
        # iterate through items and build the scroll list
        for i in self.step_row_substeps:
            
            self.root.ids.header.text = '{0} Row Number {1}'.format(
                self.wk_piece_name,
                i['StepRow'])
            
            mdlist.add_widget(
                TwoLineListItem(
                    text="{}".format(i['Action']),
                    secondary_text='{0}: {1} of {2} times'.format(
                        i['Code'],
                        i['CodeStepNum'],
                        i['HowManyTimes']),
                    secondary_theme_text_color = 'Custom',
                    secondary_text_color = [0,0,0,1],
                    secondary_font_style = 'Caption',
                    bg_color=i['FontColor'],
                    theme_text_color='Custom',
                    on_release=self.knit_piece_next_step)
                )
                        
        # add list to the scroll view
        scroll = ScrollView()
        #TODO: get the scroll into the cetnter of the screen?
        scroll.add_widget(mdlist)

        # add widget to the content area
        self.root.ids.content_main.add_widget(scroll) 


    def knit_piece_button_build(self):
        # show and clear anything left in the widget
        self.widget_visible(self.root.ids.content_col)

        scroll = Builder.load_string(kv.scroll_list_widget)  
        mdlist = scroll.ids.mdlist
        
        for button in self.piece_knit_button_labels:
            
            # add a disabled item for spacer
            mdlist.add_widget(OneLineListItem(
                size_hint = (1, .25),
                disabled = True))
            
            # add the button
            button = MDRaisedButton(
                        text=button,
                        size_hint = (1,.8),
                        on_release = self.knit_piece_button_release,
                        )
                    
            mdlist.add_widget(button)
        
        self.root.ids.content_col.add_widget(scroll)


    def knit_piece_button_release(self, instance):
        '''
        '''
        if instance.text == self.piece_knit_button_previous:
            self.knit_piece_previous_step()
            
        elif instance.text == self.piece_knit_button_jump:
            self.piece_knit_jump_to_step()
            
        elif instance.text == self.piece_knit_button_next:
            self.knit_piece_next_step()
            
        self.write_wk_step_in_progress()
    
    def knit_piece_next_step(self, inst=None):
        '''
        advance to the next step
        '''
        self.knit_step_row += 1
        
        if self.knit_step_row > self.wk_piece_in_progress['EndRow']:
            self.dialog_knit_piece_reset()
            
        else:
            self.knit_piece_content_build()

    def knit_piece_previous_step(self, inst=None):
        '''
        
        '''
        # do not move steps into negative numbers
        if self.knit_step_row > 1:
            self.knit_step_row -= 1
            
        self.knit_piece_content_build()
    
    def knit_piece_reset(self, inst=None):
        '''
        reset knitting progress on a piece
        '''
        self.knit_piece_complete.dismiss()
        self.knit_step_row = 1
        self.write_wk_step_in_progress()
        self.knit_piece_build()


    def dialog_knit_piece_reset(self):
        '''
        '''
        self.knit_piece_complete = MDDialog(
            title='Reset Progress?',
            text='Click OK to reset progress or ' \
                + 'Cancel to go back to the last step',
            type='alert',
            pos_hint = {'center_x': .5, 'top': .9},
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.dialog_knit_piece_complete_dismiss,),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.knit_piece_reset
                    )])
        
        self.knit_piece_complete.open()
        
        
    def dialog_knit_piece_complete_dismiss(self, inst):
        '''
        dismiss the dialog
        '''
        self.knit_step_row -= 1
        self.knit_piece_content_build()
        
        self.knit_piece_complete.dismiss()
        
# =============================================================================
# gui build - piece edit (listing steps)    
# ============================================================================
        
    def piece_edit_build(self):
        '''
        '''
        self.piece_edit_prep(self.wk_piece_name)

        # build the code buttons and edit screen
        self.steps_code_buttons_build()
        self.step_edit_fields_build()
        
        
    def piece_edit_prep(self,piece_name):
        '''
        '''
        # set variables for the selected working piece
        self.set_piece_vars(piece_name)
        self.screen_name = self.PieceScreenName
        
        # update the toolbar title and menu items
        self.menu_build(self.piece_menu_labels) 
        
        # show and clear anything left in the widget
        self.clear_layout()


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


    def step_get_work_idx(self,step_code):
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
        self.wk_step_idx = self.step_get_work_idx(step_code)
        
        # set variable with the working step dictionary items
        self.wk_step = self.wk_piece[self.wk_step_idx]
        step = self.wk_step
        
        self.step_edit_layout.ids.code_entry.text = step['Code']
        self.step_edit_layout.ids.action_entry.text = step['Action']
        self.step_edit_layout.ids.start_entry.text = str(step['StartRow'])
        self.step_edit_layout.ids.times_entry.text = str(step['HowManyTimes'])
        self.step_edit_layout.ids.often_entry.text = str(step['HowOften'])
        
        # self.step_edit_layout.ids.font_entry.md_bg_color = step['FontColor']
        self.root.ids.header.text = 'Edit step: ' + step['Code']


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
        
        if (self.step_get_work_idx(step_code) > -1 and 
            self.step_get_work_idx(step_code) != self.wk_step_idx):
            
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
                        
            self.write_wk_piece()  
            
            self.set_project_vars(self.wk_project_name)
            self.set_piece_vars(self.wk_piece_name, self.wk_step_idx)
            
            # update the buttons
            self.steps_code_buttons_build()
    
    
    def step_delete(self):
        '''
        '''
        del self.wk_piece[self.wk_step_idx]
        
        if self.wk_piece:
            self.write_wk_piece()  
            
            self.set_project_vars(self.wk_project_name)
            self.set_piece_vars(self.wk_piece_name)
            
            # update the buttons
            self.piece_edit_build()
        else:
            self.create_step()
        
# =============================================================================
# color picker 
# =============================================================================
    def color_picker_open(self):
        '''
        '''
        self.color_picker = MDColorPicker(
            size_hint=(0.45, 0.85),
            default_color=self.wk_step['FontColor'],
            type_color='HEX'
            
            )
        self.color_picker.open()
        self.color_picker.bind(on_select_color=self.on_select_color,
                               on_release=self.get_selected_color,)


    def update_color(self, color: list) -> None:
        '''
        '''
        self.wk_step['FontColor'] = color
        # self.step_edit_layout.ids.font_entry.md_bg_color = color
        self.step_save()


    def get_selected_color(self,
                           instance_color_picker: MDColorPicker,
                           type_color: 'str',
                           selected_color: Union[list, str]):
        '''
        '''
        self.update_color(selected_color[:-1] + [1])
        self.color_picker.dismiss()

        if self.color_picker_dialog:
            self.color_picker_dialog.dismiss()


    def color_picker_dismiss(self,inst):
        '''
        '''
        self.color_picker.dismiss()


    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''
        Called when a gradient image is clicked.
        '''
        

    def dialog_color_picker_open(self):
        '''
        popup dialog used to edit a field (e.g., project name)
        '''
        self.color_picker_dialog = MDDialog(
            title='Click a color to select',
            text='Click "More Colors" to select a different color',
            type="custom",
            pos_hint = {'center_x': .5, 'top': .9},
            content_cls=ColorPickerDialog(),
            )
        
        self.color_picker_dialog.open()
        
        
    def dialog_color_picker_save(self, inst):
        '''
        save the color selected in the color picker dialog
        '''
        self.update_color(inst.md_bg_color)
        self.color_picker_dialog.dismiss()


# =============================================================================
# settings page
# =============================================================================
    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        
        self.app_settings_label = 'App Settings'

        config.setdefaults(self.app_settings_label, 
                           {'style': 'Dark', 
                            'palette': 'Gray',
                            'hue': '500',
                            'color_select1': 'e0f2f1ff',# Teal 50
                            'color_select2': 'efebe9ff',# Brown 50
                            'color_select3': 'ffffffff',# White
                            'color_select4': 'bbdefbff',# Blue
                            'color_select5': 'f8bbd0',# Pink
                            'dropbox_token': ''})
        
   
    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settings.add_json_panel(self.app_settings_label, self.config, data=kv.settings_json)
        

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        if section == self.app_settings_label:
            if key == "style":
                self.theme_cls.theme_style = value
            elif key == 'palette':
                self.theme_cls.primary_palette = value
            elif key == 'hue':
                self.theme_cls.primary_hue = value
            elif key == 'color_select1':
                self.color_select1 = \
                    utils.get_color_from_hex(value)[:-1] + [1]                
            elif key == 'color_select2':
                self.color_select2 = \
                    utils.get_color_from_hex(value)[:-1] + [1]                
            elif key == 'color_select3':
                self.color_select3 = \
                    utils.get_color_from_hex(value)[:-1] + [1]                
            elif key == 'color_select4':
                self.color_select4 = \
                    utils.get_color_from_hex(value)[:-1] + [1]                
            elif key == 'color_select5':
                self.color_select5 = \
                    utils.get_color_from_hex(value)[:-1] + [1]    
                    
            elif key == 'dropbox_token':
                self.dropbox_token = value


    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        super(KnitApp, self).close_settings(settings)


    def set_settings_vars(self):
        '''
        set variables to use the options from settings config
        '''
        
        # define custom settings options
        self.settings_cls = SettingsWithTabbedPanel

        self.theme_cls.theme_style = self.config.get(self.app_settings_label,
                                                      'style')
        self.theme_cls.primary_palette = self.config.get(self.app_settings_label,
                                                      'palette')
        
        self.color_select1 = utils.get_color_from_hex(
            self.config.get(self.app_settings_label,
                            'color_select1'))[:-1] + [1]
        self.color_select2 = utils.get_color_from_hex(
            self.config.get(self.app_settings_label,
                            'color_select2'))[:-1] + [1]
        self.color_select3 = utils.get_color_from_hex(
            self.config.get(self.app_settings_label,
                            'color_select3'))[:-1] + [1]
        self.color_select4 = utils.get_color_from_hex(
            self.config.get(self.app_settings_label,
                            'color_select4'))[:-1] + [1]
        self.color_select5 = utils.get_color_from_hex(
            self.config.get(self.app_settings_label,
                            'color_select5'))[:-1] + [1]
        
        self.dropbox_token = self.config.get(self.app_settings_label,
                                             'dropbox_token')

# =============================================================================
# create a compressed backup and save to dropbox
# =============================================================================



    # compress file function
    def zip_file(self,file_path):
        compress_file = zipfile.ZipFile(file_path + '.zip', 'w')
        compress_file.write(file_path, compress_type=zipfile.ZIP_DEFLATED)
        compress_file.close()
    
    
    # Declare the function to return all file paths of the particular directory
    def zip_get_file_paths(self,dir_name):
        # setup file paths variable
        file_paths = []
    
        # Read all directory, subdirectories and file lists
        for root, directories, files in os.walk(dir_name):
            for filename in files:
                # Create the full file path by using os module.
                file_path = os.path.join(root, filename)
                file_paths.append(file_path)
    
        # return all paths
        return file_paths
    
    
    def zip_dir(self,dir_path, file_paths):
        # write files and folders to a zipfile
        compress_dir = zipfile.ZipFile(dir_path + '.zip', 'w')
        with compress_dir:
            # write each file separately
            for file in file_paths:
                compress_dir.write(file)


    def project_backup(self):
        
        os.chdir(self.data_dir)
        
        path = self.wk_project_name
        files_path = self.zip_get_file_paths(path)

        self.zip_dir(path, files_path)
        
        zip_path = self.wk_project_name + '.zip'
        backup_path = os.path.join('_backups', zip_path)
        os.rename(zip_path,backup_path)
        
        dropbox_access_token = self.dropbox_token
        
        dropbox_path = "/" + zip_path
        
        client = dropbox.Dropbox(dropbox_access_token)
        client.files_upload(open(backup_path, "rb").read(), 
                            dropbox_path,
                            mode=dropbox.files.WriteMode.overwrite)

        MDDialog(
            title='Backup Complete',
            text='{} has been backed up to Dropbox'.format(
                self.wk_project_name),
            pos_hint = {'center_x': .5, 'top': .9}).open()

# =============================================================================
# build application
# =============================================================================
    def build(self):
        '''
        '''
        self.set_app_vars()   
        self.root_build()
        


if __name__ == '__main__':
    KnitApp().run()