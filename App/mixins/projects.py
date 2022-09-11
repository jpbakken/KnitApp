#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:41:20 2022

@author: jpbakken
"""
import os
import shutil

# from kivymd.uix.snackbar import Snackbar

class Projects():
    '''
    '''
# =============================================================================
# data read and write functions
# =============================================================================
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


# =============================================================================
# application actions
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
# project backups
# =============================================================================
    def project_backup(self):
        '''
        authenticate and process backup in a thread
        --go through 2factor authenticate if needed
        '''
        self.icloud_action = 'backup'
        self.icloud_thread_start(self.icloud_auth)
        
        # if an untrusted session is returned, go through 2f auth
        if self.icloud:
            if not self.icloud.is_trusted_session:
                self.dialog_icloud_auth()


    def project_del_local_backup(self,):
        '''
        keep only number of backups specified in config settings
        '''
        files = os.listdir(self.wk_project_backup_dir)
        backups = []
        for f in files:
            if f.split('.')[-1] == 'zip':
                backups.append(f)
                
                
        backups.sort(reverse=True)
        
        for idx, backup in enumerate(backups):
            if idx >= int(self.backups_local):
                os.remove(os.path.join(self.wk_project_backup_dir,
                                       backup))


    def project_del_icloud_backup(self):
        '''
        keep only number of backups specified in config settings
        '''
        files = self.icloud.drive[self.app_name][self.wk_project_name].dir()
        backups = []
        for f in files:
            if f.split('.')[-1] == 'zip':
                backups.append(f)
                
        backups.sort(reverse=True)
        
        for idx, backup in enumerate(backups):
            if idx >= int(self.backups_icloud):
                self.icloud.drive[self.app_name]\
                    [self.wk_project_name][backup].delete()
