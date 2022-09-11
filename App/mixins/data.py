#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:04:58 2022

@author: jpbakken
"""

from kivymd.app import MDApp
import shutil
import os
import json

class KnitData():
    
    
    def set_data_dir(self):
        '''
        set the data directory to the user data directory for the app
        
        copy sample files from app data directory if user directory is empty
        '''
        app = MDApp.get_running_app()
        self.data_dir = app.user_data_dir
        self.copy_data_dir()

        self.encrypted_filepath = os.path.join(self.data_dir
                                               ,'_cookies','.tree')


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
                

    def read_piece(self):
        '''
        '''
        with open(self.wk_piece_filename, 'r') as json_file:     
              self.wk_piece = json.load(json_file)

                    
    def get_project_list(self):
        '''
        get and sort project list from the app data directory
        '''
        self.project_list = [d for d in next(os.walk(self.data_dir))[1] \
                             if d not in [self.backup_dirname,
                                          '_cookies']]
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
        

