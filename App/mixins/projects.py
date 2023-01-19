#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:41:20 2022

@author: jpbakken
"""
import os
import shutil
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from kivymd.uix.button import MDRaisedButton
import json

import mixins.layout as kv
from itertools import compress
from kivy.lang import Builder
# from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import TwoLineListItem

# from kivymd.uix.snackbar import Snackbar

class Projects():
    '''
    Methods related to project data, broken into sections based on action:
        data read and write functions
        --load project data into memory from data files/direcotries
        --save project data into directory/file schema
        --methods for projects, pieces, steps, kniting, work-in-progress
        
        project-level and piece-level variables
        create/copy/delete projects, pieces, and steps
        project page (listing pieces)
        edit piece (listing steps)
        substep fuctions used while knitting
        
    '''
    knit_piece_complete = None
    knit_step_row = None
    # wk_piece_in_progress = None

# =============================================================================
# data read and write functions
# =============================================================================
    def get_project_list(self):
        '''
        get and sort project list from the app data directory
        '''
        self.project_list = [d for d in next(os.walk(self.data_dir))[1] \
                             if d not in [self.backup_dirname,
                                          self.restore_dirname,
                                          '_cookies']]
        self.project_list.sort()


    def get_wk_pieces_list(self):
        '''
        get and sort pieces list from the working project directory
        '''
        self.wk_pieces_list = os.listdir(self.wk_pieces_dir)
        self.wk_pieces_list = [name.split('.')[0] for name in self.wk_pieces_list]

        self.wk_pieces_list.sort()

    def read_piece(self):
        '''
        '''
        with open(self.wk_piece_filename, 'r') as json_file:     
              self.wk_piece = json.load(json_file)

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
        self.wk_piece.sort(key=self.sort_steps_second)
        self.wk_piece.sort(key=self.sort_steps)

        with open(self.wk_piece_filename, 'w') as f:
            json.dump(self.wk_piece, f)
               

    def sort_steps(self, e):
        return e['StartRow']

    def sort_steps_second (self, e):
        return e['Code']

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
# project-level and piece-level variables
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
        
        self.wk_project_backup_dir = os.path.join(self.data_dir,
                                                  self.backup_dirname,
                                                  self.wk_project_name)

        if not os.path.exists(self.wk_project_backup_dir):
            os.makedirs(self.wk_project_backup_dir)

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


# =============================================================================
# create/copy/delete projects, pieces, and steps
# =============================================================================
    def create_project(self):
        '''
        use edit field dialog to create a new project
        '''
        self.edit_field_check_list = self.project_list
        self.edit_field_text = ''
        self.dialog_field_build()


    def copy_project(self):
        '''
        '''
        self.edit_field_name = 'Copied Project Name'
        self.create_project()

        # Snackbar(text=self.wk_project_name).open()
        
        
    def delete_project(self):
        '''
        '''
        shutil.rmtree(self.wk_project_data_dir)
        shutil.rmtree(self.wk_project_backup_dir)


    def create_piece(self):
        '''
        use edit field dialog to create a new piece
        '''
        self.edit_field_check_list = self.wk_pieces_list
        self.edit_field_text = ''
        self.dialog_field_build()


    def copy_piece(self):
        '''
        '''
        self.edit_field_name = 'Copied Piece Name'
        self.create_piece()
        
        
    def delete_piece(self):
        '''
        '''
        os.remove(self.wk_piece_filename)
        
        # Snackbar(text='hello').open()
        

    def create_step(self, step):
        '''
        '''
        step['Code'] = step['Code'] + str(len(self.wk_piece)+1)
                
        self.wk_piece.append(step)
        
        self.wk_step_idx = self.step_get_work_idx(step['Code'])

        self.set_piece_filenames()
        
        self.write_wk_piece()
        
        self.piece_edit_build()
        
        self.step_edit(step['Code'])



    def step_delete(self):
        '''
        '''
        del self.wk_piece[self.wk_step_idx]
        
        if self.wk_piece:
            self.write_wk_piece()  
            
            self.set_project_vars(self.wk_project_name)
            self.set_piece_vars(self.wk_piece_name)
            self.wk_step_idx = 0
            
            # update the buttons
            self.piece_edit_build()
        else:
            self.create_step(self.new_step_dict.copy())


# =============================================================================
# project page (listing pieces)
# =============================================================================
    def project_build(self):
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
        self.set_project_vars(self.wk_project_name)
        self.screen_name = self.ProjectScreenName


        # update the toolbar title and menu items
        self.menu_build(self.project_menu_labels)            
        
        # build the list of pieces
        self.item_list_build(self.wk_pieces_list,
                             self.root.ids.content_main)
        
        # build the edit pieces buttons
        self.project_pieces_buttons_build()
        
    def project_pieces_buttons_build(self):
        '''
        build buttons in content_col on the pieces page
        '''
        self.content_col_button_build(self.project_button_labels)
        
        
# =============================================================================
# edit piece (listing steps)    
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
        self.set_piece_vars(piece_name, self.wk_step_idx)
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
            
            self.wk_step_idx = self.step_get_work_idx(step['Code'])
            
            self.set_project_vars(self.wk_project_name)
            self.set_piece_vars(self.wk_piece_name, self.wk_step_idx)
            
            # update the buttons
            self.piece_edit_build()
    
    
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
        
        self.write_wk_step_in_progress()
        
        self.widget_visible(self.root.ids.content_main)

        self.get_current_substeps()
        
        # build the list of pieces
        mdlist = MDList()        
        mdlist.add_widget(TwoLineListItem(disabled=True))
        
        # iterate through items and build the scroll list        
        for i in self.step_row_substeps:
            
            self.root.ids.header.text = '{0} Row Number {1} of {2}'.format(
                self.wk_piece_name,
                i['StepRow'],
                self.wk_piece_in_progress['EndRow'])
            
            two_line_widget = TwoLineListItem(
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
                        
            mdlist.add_widget(two_line_widget)
            
        # add list to the scroll view
        scroll = ScrollView(do_scroll=False)
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
    
    
    def knit_piece_reset_work_in_progress(self):
        '''
        '''
        
        self.knit_step_row = 1
        self.write_wk_step_in_progress()
        
    
    def knit_piece_reset(self, inst=None):
        '''
        reset knitting progress on a piece
        '''
        if self.knit_piece_complete:
            self.knit_piece_complete.dismiss()
                    
        if self.knit_step_row > self.wk_piece_in_progress['EndRow']:
            self.piece_callback(self.piece_menu_back_to_project)
            self.knit_piece_reset_work_in_progress()
        else:
            self.knit_piece_reset_work_in_progress()
            self.knit_piece_build() 
            

    def piece_knit_jump_to_step(self):
        '''
        '''
        self.edit_field_name = self.piece_knit_button_jump
        self.edit_field_check_list = [0]
        self.edit_field_text = str(self.knit_step_row)

        self.dialog_field_build()
