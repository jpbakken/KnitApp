#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: jpbakken
"""
#TODO: add encryption back to icloud username/password
#TODO: restore from backup
    # local or icloud backup?
#TODO: Delete piece prompts delete package
#TODO: when new step is created, that step should be selected
#TODO: when piece is creted, problems with steps if teh first step doesn't get renamed


from mixins.colorpicker import ColorPicker
from mixins.backups import Backups
from mixins.projects import Projects
from mixins.settings import Settings
from mixins.uix import Uix
from mixins.vars import Vars
from mixins.zip import Zip
from kivymd.app import MDApp


class KnitApp(ColorPicker,
              Backups,
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
    
    
