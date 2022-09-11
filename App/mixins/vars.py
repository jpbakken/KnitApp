#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 10:40:36 2022

@author: jpbakken
"""
import kv
# from cryptography.fernet import Fernet
from kivy.lang import Builder



# =============================================================================
# variables that get set when objects are selected (projects, pieces, etc)        
# =============================================================================
class AppVars():
    
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

        # get the list of saved projects
        self.get_project_list()

        # import the layout strings
        self.root= Builder.load_string(kv.main_screen)
        self.step_edit_layout = Builder.load_string(kv.step_edit_screen)

        # set name of the settings menu item
        self.menu_item_settings = 'Settings'

        # set names for the root toolbar menu
        self.root_menu_create_project = 'Create New Project'
        self.root_menu_icloud_auth = 'Authenticate iCloud'
        self.root_menu_labels = [self.root_menu_create_project,
                                  self.root_menu_icloud_auth,
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
        
        self.icloud_read_encrypted()
