#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:52:03 2022

@author: jpbakken
"""
import os
import kv
from mixins.layout import EditFieldDialog

from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.metrics import dp


class Uix():
    '''
    '''
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