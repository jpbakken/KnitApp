#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:52:03 2022

@author: jpbakken
"""
import os

import mixins.layout as kv
from mixins.layout import EditFieldDialog

from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.uix.snackbar import Snackbar

class Uix():
    '''
    '''
    edit_field_dialog = None
    confirm_dialog = None

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
        
        # get the list of saved projects
        self.get_project_list()
        
        self.menu_build(self.root_menu_labels)
        
        self.item_list_build(self.project_list,
                             self.root.ids.content_main)

    def set_uix_vars(self):
        '''
        '''
        
        # set name of the settings menu item
        self.menu_item_settings = 'Settings'

        # set names for the root toolbar menu
        self.root_menu_create_project = 'Create New Project'
        self.root_menu_icloud_auth = 'Authenticate iCloud'
        self.root_menu_labels = [self.root_menu_create_project,
                                  self.root_menu_icloud_auth,
                                 self.menu_item_settings]


        # project toolbar menu
        self.project_menu_add_piece = 'Add Piece'
        self.project_menu_edit_name = 'Edit Name'
        self.project_menu_project_copy = 'Copy Project'
        self.project_menu_project_delete = 'Delete Project'
        self.project_menu_back_to_root = 'Back to Projects'
        self.project_menu_project_backup = 'Backup Project'
        
        
        
        self.project_menu_labels = [self.project_menu_back_to_root]

        self.project_button_labels = [self.project_menu_add_piece,
                                      self.project_menu_edit_name,
                                      self.project_menu_project_copy,
                                      self.project_menu_project_delete,
                                      self.project_menu_project_backup]

        # piece select list menu
        self.piece_menu_knit = 'Knit Piece'
        self.piece_menu_edit_steps = 'Edit Piece'
        self.piece_menu_copy_piece = 'Copy Piece'
        self.piece_menu_delete_piece = 'Delete Piece'
        
        self.list_menu_labels_piece = [self.piece_menu_knit,
                                       self.piece_menu_edit_steps,
                                       self.piece_menu_copy_piece,
                                       self.piece_menu_delete_piece]

        # piece page toolbar menu
        self.piece_menu_add_step = 'Add New Step'
        self.piece_menu_copy_step = 'Copy Selected Step'
        self.piece_menu_delete_step = 'Delete Selected Step'
        self.piece_menu_back_to_project = 'Back to Project Pieces'
        self.piece_menu_edit_name = 'Edit Piece Name'
        
        self.piece_menu_labels = [self.piece_menu_add_step,
                                  self.piece_menu_copy_step,
                                  self.piece_menu_delete_step,
                                  self.piece_menu_knit,
                                  self.piece_menu_edit_name,
                                  self.piece_menu_back_to_project,]
        
        
        self.piece_knit_menu_reset = 'Reset progress'

        self.piece_knit_menu_labels = [self.piece_knit_menu_reset,
                                       self.piece_menu_edit_steps,
                                       self.piece_menu_back_to_project,
                                       ]
        
        self.piece_knit_button_previous = 'Previous Step'
        self.piece_knit_button_jump = 'Jump to Step'
        self.piece_knit_button_next = 'Next Step'
        
        self.piece_knit_button_labels = [self.piece_knit_button_previous,
                                         self.piece_knit_button_jump,
                                         self.piece_knit_button_next]

        

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
            self.menu_callback(menu_item)            
        
        else:
            Snackbar(text=menu_item).open()


    def item_list_menu_on_release(self, instance):
        '''
        '''
        # if on the main screen, click through to the list of project pieces
        if self.screen_name == self.RootScreenName:
            self.set_project_vars(instance.text)
            self.project_build()

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
# content_col buttons build
# =============================================================================

    def content_col_button_build(self,
                                 button_list,
                                 padding_hint=.25
                                 ):

        # show and clear anything left in the widget
        self.widget_visible(self.root.ids.content_col)

        scroll = Builder.load_string(kv.scroll_list_widget)  
        mdlist = scroll.ids.mdlist
        
        for button in button_list:
            
            # add a disabled item for spacer
            mdlist.add_widget(OneLineListItem(
                size_hint = (.8, padding_hint),
                disabled = True))
            
            # add the button
            button = MDRaisedButton(
                        text=button,
                        size_hint = (.8,.8),
                        on_release = self.content_col_button_on_release,
                        )
                    
            mdlist.add_widget(button)
        
        self.root.ids.content_col.add_widget(scroll)


    def content_col_button_on_release(self, inst):
        '''
        '''
        self.menu_callback(inst.text)
        
        
# =============================================================================
# edit field dialog box build
# =============================================================================
    def dialog(self,
                title='Failed', 
                text='Verification failed. Please try again.'):
        
        MDDialog(title=title,
                  text=text,
                  pos_hint = {'center_x': .5, 'top': .9}).open()


    def dialog_confirm(self,
                       title,
                       text,):
    
        self.confirm_dialog = MDDialog(
            title=title,
            text=text,
            pos_hint = {'center_x': .5, 'top': .9},
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=self.dialog_confirm_dismiss),
                MDFlatButton(
                    text="OK",
                    on_release=self.dialog_confirm_ok)])
            
        self.confirm_dialog.open()
        
        
    def dialog_confirm_dismiss(self, inst):
        '''
        '''
        self.confirm_dialog.dismiss()
        
        
    def dialog_confirm_ok(self, inst):
        '''
        '''
        self.menu_callback(self.confirm_dialog.title)
        self.confirm_dialog.dismiss()

        
        
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
            # creating or editing a project name
            if 'Project Name' in self.edit_field_name:
                edit_field.helper_text=\
                    'There can be only one...name must be unique'
                self.dialog_project_name_save(new_value)

            # creating or editing a piece name
            elif 'Piece Name' in self.edit_field_name:
                self.dialog_piece_name_save(new_value)
                
            # jumping to a specified row
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
            if not os.path.exists(new_path + '/Pieces'):
                os.makedirs(new_path + '/Pieces')
            if not os.path.exists(new_path + '/Substeps'):
                os.makedirs(new_path + '/Substeps')
                if not os.path.exists(new_path + '/WorkInProgress'):
                    os.makedirs(new_path + '/WorkInProgress')
                
        elif 'Copied' in self.edit_field_name:
            self.copy_data_dir(source_dir = self.wk_project_data_dir, 
                               target_dir = new_path)
                
        # refresh the list of saved projects
        self.get_project_list()

        self.project_build()
        
        
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
            self.create_step(self.new_step_dict.copy())

        elif 'Copied' in self.edit_field_name:
            self.wk_step_idx = 0
            self.set_piece_filenames()
            self.write_wk_piece()
            self.piece_edit_build()

            
    def dialog_piece_jump_save(self,new_value):
        '''
        on the knit page, jump to a specific step
        '''
        self.edit_field_dialog.dismiss()
        
        self.knit_step_row = int(new_value)
        self.knit_piece_content_build()


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
            self.root_callback(menu_item)

        elif self.screen_name == self.ProjectScreenName:
            self.project_callback(menu_item)

        elif self.screen_name in [self.PieceScreenName,
                                  self.PieceKnitScreenName]:
            self.piece_callback(menu_item)


    def root_callback(self, menu_item):
        '''
        '''
        if menu_item == self.root_menu_create_project:
            self.edit_field_name = 'New Project Name'
            self.create_project()
            
        if menu_item == self.root_menu_icloud_auth:
            self.dialog_icloud_login()


    def project_callback(self, menu_item):
        '''
        '''
        
        if menu_item == self.project_menu_add_piece:
            self.edit_field_name = 'New Piece Name'
            self.create_piece()
        
        elif menu_item == self.project_menu_edit_name:
            self.edit_field_name = 'Edit Project Name'
            self.dialog_field_build()

        elif menu_item == self.project_menu_back_to_root:
            self.root_build()
            
        elif menu_item == self.project_menu_project_copy:
            self.copy_project()
            
        elif menu_item == self.project_menu_project_delete:
            # button is called "Delete" - opens confirmation dialog
            self.dialog_confirm(
                title=self.delete_project_title,
                text=self.delete_project_text)
        
        elif menu_item == self.delete_project_title:
            self.delete_project()
            self.root_build()
            
        elif menu_item == self.delete_piece_title:
            self.delete_piece()
            self.project_build()

        elif menu_item == self.project_menu_project_backup:
            self.project_backup()
    
        elif menu_item == self.piece_menu_knit:
            self.knit_piece_build() 
            
        elif menu_item == self.piece_menu_edit_steps:
            self.wk_step_idx = 0
            self.piece_edit_build()

        elif menu_item == self.piece_menu_copy_piece:
            self.copy_piece()
        
        elif menu_item == self.piece_menu_delete_piece:
            # button is called "Delete" - opens confirmation dialog
            self.dialog_confirm(
                title=self.delete_piece_title,
                text=self.delete_piece_text)


    def piece_callback(self, menu_item):
        '''
        '''

        if menu_item == self.piece_menu_add_step:
            self.create_step(self.new_step_dict.copy())

        elif menu_item == self.piece_menu_copy_step:
            self.create_step(self.wk_piece[self.wk_step_idx].copy())
            
        elif menu_item == self.piece_menu_delete_step:
            self.step_delete()
                
        elif menu_item == self.piece_menu_knit:
            self.knit_piece_build()
            self.knit_piece_reset()

        elif menu_item == self.piece_menu_edit_name:
            self.dialog_field_build()

        elif menu_item == self.piece_menu_edit_steps:
            self.wk_step_idx = 0
            self.piece_edit_build()
        

        elif menu_item == self.piece_menu_back_to_project:
            
            if self.screen_name == self.PieceScreenName:
                self.step_save()
                
                if self.validation_error == False:
                    self.project_build()
                    
            elif self.screen_name == self.PieceKnitScreenName:
                self.project_build()

        elif menu_item == self.piece_knit_menu_reset:
            self.dialog_knit_piece_reset()

