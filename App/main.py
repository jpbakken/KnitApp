#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: jpbakken
"""
#TODO:
    # add encryption back to icloud username/password
#TODO: delete project
#TODO: copy prjoect
    
#TODO: delete piece
#TODO: copy piece
#TODO: restore from backup
    # local or icloud backup

import kv
from mixins.zip import Zip
from mixins.icloud import iCloud
from mixins.knit import Knit
from mixins.vars import AppVars
from mixins.data import KnitData
from mixins.projects import Projects
from mixins.pieces import Pieces
from mixins.uix import Uix
from mixins.menu import Menu
from mixins.colorpicker import ColorPicker

from kivy.uix.settings import SettingsWithTabbedPanel
import kivy.utils as utils
from kivymd.app import MDApp


class KnitApp(ColorPicker,
              KnitData,
              Uix,
              iCloud,
              Knit,
              Pieces,
              Projects,
              Menu,
              AppVars,
              Zip, 
              MDApp):
    
# =============================================================================
# initialize variables
# =============================================================================
    use_kivy_settings = False
    color_picker = None
    edit_field_dialog = None
    knit_piece_complete = None
    icloud = None
    icloud_action = None
    backup_dirname = '_backups'
    app_name = 'KnitRows'    

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
# settings page
# =============================================================================
    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        
        self.app_settings_label = 'App Settings'
        self.backup_settings_label = 'Backups'
        
        config.setdefaults(self.app_settings_label, 
                           {'style': 'Dark', 
                            'palette': 'Gray',
                            'hue': '500',
                            'color_select1': 'e0f2f1ff',# Teal 50
                            'color_select2': 'efebe9ff',# Brown 50
                            'color_select3': 'ffffffff',# White
                            'color_select4': 'bbdefbff',# Blue
                            'color_select5': 'f8bbd0',# Pink
                            })
        
        config.setdefaults(self.backup_settings_label, 
                           {'backups_local': 3, 
                            'backups_icloud': 10,})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settings.add_json_panel(self.app_settings_label, 
                                self.config, 
                                data=kv.app_settings_json)
        
        settings.add_json_panel(self.backup_settings_label, 
                                self.config, 
                                data=kv.backup_settings_json)


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

        if section == self.backup_settings_label:
            if key =='backups_local':
                self.backups_local = value
            if key =='backups_icloud':
                self.backups_icloud = value                

                    
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
        
        self.backups_icloud = self.config.get(self.backup_settings_label,
                                              'backups_icloud')
        self.backups_local = self.config.get(self.backup_settings_label,
                                              'backups_local')



        



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