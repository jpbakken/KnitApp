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

from mixins.zip import Zip
from mixins.icloud import iCloud
from mixins.knit import Knit
from mixins.vars import AppVars
from mixins.projects import Projects
from mixins.pieces import Pieces
from mixins.uix import Uix
from mixins.colorpicker import ColorPicker
from mixins.settings import Settings
from kivymd.app import MDApp


class KnitApp(ColorPicker,
              Uix,
              iCloud,
              Knit,
              Pieces,
              Projects,
              AppVars,
              Settings,
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
# build application
# =============================================================================
    def build(self):
        '''
        '''
        self.app = MDApp.get_running_app()
        self.set_app_vars()   
        self.root_build()
        

if __name__ == '__main__':
    KnitApp().run()