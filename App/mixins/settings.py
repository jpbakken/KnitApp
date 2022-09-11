#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 11:18:10 2022

@author: jpbakken
"""
import kivy.utils as utils
from kivy.uix.settings import SettingsWithTabbedPanel


class Settings():
# =============================================================================
# settings page
# =============================================================================

    # def close_settings(self, settings=None):
    #     """
    #     The settings panel has been closed.
    #     """
    #     super(KnitApp, self).close_settings(settings)

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
                                data=app_settings_json)
        
        settings.add_json_panel(self.backup_settings_label, 
                                self.config, 
                                data=backup_settings_json)


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


app_settings_json = '''
[
    {"type": "string",
     "title": "Theme Style",
     "desc": "Choose the theme style: Light/Dark",
     "section": "App Settings",
     "key": "style"},
    {"type": "string",
     "title": "Theme Primary Palette",
     "desc": "Choose the base color: Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange, Brown, Gray, BlueGray",
     "section": "App Settings",
     "key": "palette"},
    {"type": "string",
     "title": "Theme Primary Hue",
     "desc": "Choose the hue: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, A100, A200, A400, A700",
     "section": "App Settings",
     "key": "hue"},
    {"type": "color",
     "title": "Default Color Button 1",
     "desc": "Set default color button options for step settings",
     "section": "App Settings",
     "key": "color_select1"},
    {"type": "color",
     "title": "Default Color Button 2",
     "desc": "Set default color button options for step settings",
     "section": "App Settings",
     "key": "color_select2"},
    {"type": "color",
      "title": "Default Color Button 3",
      "desc": "Set default color button options for step settings",
      "section": "App Settings",
      "key": "color_select3"},
    {"type": "color",
      "title": "Default Color Button 4",
      "desc": "Set default color button options for step settings",
      "section": "App Settings",
      "key": "color_select4"},
    {"type": "color",
      "title": "Default Color Button 5",
      "desc": "Set default color button options for step settings",
      "section": "App Settings",
      "key": "color_select5"}
]
'''

backup_settings_json = '''

[
    {"type": "numeric",
      "title": "Local backups to keep",
      "desc": "How many local backups should be kept?",
      "section": "Backups",
      "key": "backups_local"},
    {"type": "numeric",
      "title": "iCloud backups to keep",
      "desc": "How many iCloud backups should be kept?",
      "section": "Backups",
      "key": "backups_icloud"}
]
'''
