#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:41:39 2022

@author: jpbakken
"""
import os
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList
from kivymd.uix.button import MDRaisedButton
import json


class Pieces():
    '''
    '''
# =============================================================================
# data read and write functions
# =============================================================================
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
        self.wk_piece.sort(key=self.sort_steps)

        with open(self.wk_piece_filename, 'w') as f:
            json.dump(self.wk_piece, f)
               

    def sort_steps(self, e):
        return e['StartRow']


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

# =============================================================================
# application actions
# =============================================================================
    def create_piece(self):
        '''
        use edit field dialog to create a new piece
        '''
        self.edit_field_name = 'New Piece Name'
        self.edit_field_check_list = self.wk_pieces_list
        self.edit_field_text = ''
        self.dialog_field_build()


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
    
    
