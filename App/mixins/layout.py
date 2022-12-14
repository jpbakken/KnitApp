#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 10:34:03 2022

@author: jpbakken
"""
from kivymd.uix.boxlayout import MDBoxLayout

class EditFieldDialog(MDBoxLayout):
    pass


class iCloudCredentialsDialog(MDBoxLayout):
    pass


class ColorPickerDialog(MDBoxLayout):
    pass



main_screen = '''
#:kivy 1.8.0

MDGridLayout:
    cols: 1
    md_bg_color: app.theme_cls.primary_dark

    MDTopAppBar:
        id: toolbar
        title: 'Menu Title'
        pos_hint: {'center_x':0.5, 'top':1}

    # buffer area above the content panel
    Label:
        id: header
        size_hint_y: .1
        pos_hint: {'center_x':0.5, 'top':1}


    # grid add buffer areas to the sides
    MDGridLayout:
        cols: 3

        # buffer area to the left of the content panel
        MDBoxLayout:
            size_hint_x: .05

        # main content area
        MDGridLayout:
            id: content
            size_hint_y: .8
            cols: 1
            
            MDGridLayout:
                id: content_cols
                cols:3
                
                MDGridLayout: # lcol
                    id: content_col
                    size_hint: (.2, 1)
                    cols: 1
                    
                MDGridLayout:
                    id: content_buff
                    size_hint: (.05,1)
                    
                MDGridLayout: # rcol
                    id: content_main
                    cols: 1

        # buffer area to the right of the content panel
        MDBoxLayout:
            size_hint_x: .05

    # buffer area below the content panel
    MDBoxLayout:
        size_hint_y: .1
        # md_bg_color: app.theme_cls.primary_dark


<EditFieldDialog>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None

    MDTextField:
        id: edit_field
        hint_text: app.edit_field_name
        text: app.edit_field_text
        helper_text: 'There can be only one...name must be unique'
        helper_text_mode: 'on_error'
   
    
<iCloudCredentialsDialog>
    orientation: "vertical"
    spacing: "12dp"
    height: "120dp"

    size_hint_y: None
    
    
    MDTextField:
        id: apple_id
        hint_text: 'Enter Apple Id'
        text: app.apple_id

    MDTextField:
        id: apple_password
        hint_text: 'Enter Apple Password'
        text: app.apple_password    
        password: True
        
        
<ColorPickerDialog>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDGridLayout:
        id: list_grid
        cols: 5
        size_hint: (.6,.8)
        pos_hint: {'center_x': .5, 'center_y': .5}
        
        # row 1
        MDRaisedButton:
            id: color_select1
            text: 'Set Color'
            md_bg_color: app.color_select1
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size: more_colors.size
            on_release: app.dialog_color_picker_save(self)

        MDBoxLayout:
            size_hint_x: .1

        MDRaisedButton:
            id: color_select2
            text: 'Set Color'
            md_bg_color: app.color_select2
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size: more_colors.size
            on_release: app.dialog_color_picker_save(self)
            
        MDBoxLayout:
            size_hint_x: .1

        MDRaisedButton:
            id: color_select3
            text: 'Set Color'
            md_bg_color: app.color_select3
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size: more_colors.size
            on_release: app.dialog_color_picker_save(self)
        
        #row 2
        MDRaisedButton:
            id: color_select4
            text: 'Set Color'
            md_bg_color: app.color_select4
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size: more_colors.size
            on_release: app.dialog_color_picker_save(self)
            
        MDBoxLayout:
            size_hint_x: .1
            
        MDRaisedButton:
            id: color_select5
            text: 'Set Color'
            md_bg_color: app.color_select5
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size: more_colors.size
            on_release: app.dialog_color_picker_save(self)

        MDBoxLayout:
            size_hint_x: .1

        MDRaisedButton:
            id: more_colors
            text: 'More Colors'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_release: app.color_picker_open()


'''

scroll_list_widget = '''

ScrollView:    
    id: scroll
    MDList:
        id: mdlist


'''


step_edit_screen = '''

MDGridLayout:
    id: list_grid
    cols: 1
    size_hint: (.6,.8)
    pos_hint: {'center_x': .5, 'center_y': .5}

    MDTextField:
        id: code_entry
        hint_text: 'Code'
        helper_text: 'There can be only one...code must be unique within a piece'
        helper_text_mode: 'on_error'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200
        on_focus: app.step_save()

    MDTextField:
        id: action_entry
        hint_text: 'Action'
        helper_text: 'Desribe the step'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200
        on_focus: app.step_save()

    MDGridLayout:
        id: row_grid
        cols: 3
        size_hint_y: None
        height: 120

        MDTextField:
            id: start_entry
            hint_text: 'Start Row'
            helper_text: 'Start row must be a number'
            helper_text_mode: 'on_error'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_focus: app.step_save()
    
        MDTextField:
            id: often_entry
            hint_text: 'How Often to repeat the step'
            helper_text: 'How often must be a number'
            helper_text_mode: 'on_error'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_focus: app.step_save()
    
        MDTextField:
            id: times_entry
            hint_text: 'How Many Times to repeat the step'
            helper_text: 'How many times must be a number'
            helper_text_mode: 'on_error'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_focus: app.step_save()

    MDRaisedButton:
        id: font_entry
        text: 'Set Step Color'
        pos_hint: {'center_x': 0.5, 'top': 0}
        on_release: app.dialog_color_picker_open()


'''
