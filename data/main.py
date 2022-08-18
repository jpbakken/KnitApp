#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 21:21:15 2022

@author: jpbakken
"""
## Sample Python application demonstrating the
## working of FloatLayout in Kivy using .kv file
  
###################################################
# import modules
  
import kivy
import pandas as pd

# base Class of your App inherits from the App class.  
# app:always refers to the instance of your application 
from kivy.app import App
  
# module consist the floatlayout
# to work with FloatLayout first
# you have to import it
from kivy.uix.floatlayout import FloatLayout
  
# To change the kivy default settings 
# we use this module config 
from kivy.config import Config 

from kivy.properties import StringProperty


# 0 being off 1 being on as in true / false 
# you can use 0 or 1 && True or False 
Config.set('graphics', 'resizable', True)
  
  
# creating the root widget used in .kv file 
class FloatLayout(FloatLayout):
    stepcode = StringProperty('ButtonName')  
    
    def __init__(self):
        '''
        '''
        app = App.get_running_app()
        # print("app.directory = ", app.directory)
        # print("app.user_data_dir = ", app.user_data_dir)
        self.data_dir = app.user_data_dir
                # returning the instance of root class
        df = pd.read_parquet(self.data_dir + '/steps.parquet')
        
        self.stepcode = df.StepCode[1]
        
    pass
  
# creating the App class in which name
#.kv file is to be named Float_Layout.kv
class Float_LayoutApp(App):
    # def __init_(self):

    # defining build()
    def build(self):
        # app = App.get_running_app()
        # # print("app.directory = ", app.directory)
        # # print("app.user_data_dir = ", app.user_data_dir)
        # self.data_dir = app.user_data_dir
        #         # returning the instance of root class
        # df = pd.read_parquet(self.data_dir + '/steps.parquet')
        
        # self.stepcode = df.StepCode[1]
        
        return FloatLayout()
  
# run the app
if __name__ == "__main__":
    Float_LayoutApp().run()
