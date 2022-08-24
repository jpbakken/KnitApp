#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 14:37:03 2022

@author: jpbakken
"""


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
        size_hint_y: .05
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
            size_hint_y: .9
            cols: 1

        # buffer area to the right of the content panel
        MDBoxLayout:
            size_hint_x: .05

    # buffer area below the content panel
    MDBoxLayout:
        size_hint_y: .05
        # md_bg_color: app.theme_cls.primary_dark


'''

step_edit_button = '''

MDRaisedButton
    text: 'Edit Steps'
    # size_hint: (1,.8)        
    pos_hint: {'center_x': .5, 'center_y': .5}
    on_release: app.piece_steps_edit_build()

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
        helper_text: 'There can be only one...code must be unique'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200

    MDTextField:
        id: action_entry
        hint_text: 'Action'
        helper_text: 'Desribe the step'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200
    MDTextField:
        id: start_entry
        hint_text: 'Start Row'
        helper_text: 'Start row must be a number'
        helper_text_mode: 'on_error'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200
        # on_text_validate: app.step_int_type_check

    MDTextField:
        id: often_entry
        hint_text: 'How Often to repeat the step'
        helper_text: 'How often must be a number'
        helper_text_mode: 'on_error'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200

    MDTextField:
        id: times_entry
        hint_text: 'How Many Times to repeat the step'
        helper_text: 'How many times must be a number'
        helper_text_mode: 'on_error'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200

    MDTextField:
        id: font_entry
        hint_text: 'Font Color'
        helper_text: 'Font color for the step when working the project'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        #size_hint_x: None
        width: 200
'''
