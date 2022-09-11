#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: jpbakken
"""
#TODO: add encryption back to icloud username/password
#TODO: restore from backup
    # local or icloud backup

from mixins.colorpicker import ColorPicker
from mixins.icloud import iCloud
from mixins.pieces import Pieces
from mixins.projects import Projects
from mixins.settings import Settings
from mixins.uix import Uix
from mixins.vars import Vars
from mixins.zip import Zip
from kivymd.app import MDApp


class KnitApp(ColorPicker,
              iCloud,
              Pieces,
              Projects,
              Settings,
              Uix,
              Vars,
              Zip, 
              MDApp):

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