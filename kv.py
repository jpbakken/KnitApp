#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 14:37:03 2022

@author: jpbakken
"""


main_screen = '''
#:kivy 1.8.0

<EditFieldDialog>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    # height: "120dp"

    MDTextField:
        id: edit_field
        hint_text: app.edit_field_name
        text: app.edit_field_text
        helper_text: 'There can be only one...project name must be unique'
        helper_text_mode: 'on_error'
        

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


'''

knit_piece_button_labels = '''

MDGridLayout:
    cols: 1  
        
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

    MDTextField:
        id: start_entry
        hint_text: 'Start Row'
        helper_text: 'Start row must be a number'
        helper_text_mode: 'on_error'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200
        on_focus: app.step_save()

    MDTextField:
        id: often_entry
        hint_text: 'How Often to repeat the step'
        helper_text: 'How often must be a number'
        helper_text_mode: 'on_error'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200
        on_focus: app.step_save()

    MDTextField:
        id: times_entry
        hint_text: 'How Many Times to repeat the step'
        helper_text: 'How many times must be a number'
        helper_text_mode: 'on_error'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200
        on_focus: app.step_save()

    MDRaisedButton:
        id: font_entry
        text: 'Step Text Color'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_release: app.open_color_picker()


'''


settings_json = '''
[
    {
        "type": "string",
        "title": "Theme Style",
        "desc": "Choose the theme style: Light/Dark",
        "section": "App Settings",
        "key": "style"
    },
    {
        "type": "string",
        "title": "Theme Primary Palette",
        "desc": "Choose the base color: Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal, Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange, Brown, Gray, BlueGray",
        "section": "App Settings",
        "key": "palette"
    },
    {
        "type": "string",
        "title": "Theme Primary Hue",
        "desc": "Choose the hue: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, A100, A200, A400, A700",
        "section": "App Settings",
        "key": "hue"
    }
]
'''
