#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 13:58:51 2022

@author: jpbakken
"""
from kivy.uix.settings import SettingsWithTabbedPanel
import kivy.utils as utils
import kv


class Mixin:
    app_settings_label = 'App Settings'
    
# =============================================================================
# settings page
# =============================================================================
    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        
        # self.app_settings_label = 'App Settings'

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
        
   
    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settings.add_json_panel(self.app_settings_label, self.config, data=kv.settings_json)
        
        self.settings = settings

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
