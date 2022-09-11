#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:33:27 2022

@author: jpbakken
"""
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu


class Menu():
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
            
        if menu_item == self.root_menu_icloud_auth:
            self.dialog_icloud_login()


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
