#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 10:40:36 2022

@author: jpbakken
"""
import mixins.layout as kv
# from cryptography.fernet import Fernet
from kivy.lang import Builder

import shutil
import os


# =============================================================================
# variables that get set when objects are selected (projects, pieces, etc)        
# =============================================================================
class Vars():
    backup_dirname = '_backups'
    app_name = 'KnitRows'   

# =============================================================================
# data direcotry variables and processing
# =============================================================================
    def set_data_dir(self):
        '''
        set the data directory to the user data directory for the app
        
        copy sample files from app data directory if user directory is empty
        '''
         
        self.data_dir = self.app.user_data_dir
        #if target directory has no project folders 
        if not [d for d in next(os.walk(self.data_dir))[1]]:
            self.copy_data_dir(source_dir = 'data', 
                               target_dir = self.data_dir)

        self.encrypted_filepath = os.path.join(self.data_dir
                                               ,'_cookies','.tree')


    def copy_data_dir(self, source_dir, target_dir):
        '''
        if self.data_dir is empty, copy the sample data dir
        '''
        
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

# =============================================================================
# class variables
# =============================================================================
    def set_app_vars(self):
        """
        Define variables that can be used throughout
        """
 
        # key = 'sBmu4_hZR6osbj7N__jO-SfOY8Q13QSoypcXQ3_Pvp4='
        # self.fernet = Fernet(key)

        self.set_data_dir()

        # define custom settings options
        self.set_settings_vars()

        # import the layout strings
        self.root= Builder.load_string(kv.main_screen)
        self.step_edit_layout = Builder.load_string(kv.step_edit_screen)

        self.set_uix_vars()
        
        self.new_step_dict = {'Code': 'Code',
                              'StepRow': 1,
                              'Action': '',
                              'HowManyTimes': 1, 
                              'HowOften': 1, 
                              'StartRow': 1, 
                              'FontColor': self.color_select1
                              }

        self.new_wk_in_progress = {"StepRow": 1}


        self.toolbar_title = 'Projects'
        
        self.StepEditScreenName = 'stepedit'
        
        self.RootScreenName = 'root'
        self.ProjectScreenName = 'project'
        self.PieceScreenName = 'piece'
        self.PieceKnitScreenName = 'knit'
        
        self.delete_project_title = 'Delete Project'
        self.delete_project_text = \
            'This will delete all local project data,' \
            + 'including backups.' \
            + '\n\n' \
            + 'Are you sure?'

        self.delete_piece_title = 'Delete Piece'
        self.delete_piece_text = \
            'This will delete the piece and all steps.' \
            + '\n\n' \
            + 'Are you sure?'
            
        self.icloud_read_encrypted()
