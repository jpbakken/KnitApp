#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 10:53:20 2022

@author: jpbakken
"""
from mixins.layout import ColorPickerDialog
from typing import Union
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDColorPicker

class ColorPicker():
# =============================================================================
# color picker 
# =============================================================================
    def color_picker_open(self):
        '''
        '''
        self.color_picker = MDColorPicker(
            size_hint=(0.45, 0.85),
            default_color=self.wk_step['FontColor'],
            type_color='HEX'
            
            )
        self.color_picker.open()
        self.color_picker.bind(on_select_color=self.on_select_color,
                               on_release=self.get_selected_color,)


    def update_color(self, color: list) -> None:
        '''
        '''
        self.wk_step['FontColor'] = color
        # self.step_edit_layout.ids.font_entry.md_bg_color = color
        self.step_save()


    def get_selected_color(self,
                           instance_color_picker: MDColorPicker,
                           type_color: 'str',
                           selected_color: Union[list, str]):
        '''
        '''
        self.update_color(selected_color[:-1] + [1])
        self.color_picker.dismiss()

        if self.color_picker_dialog:
            self.color_picker_dialog.dismiss()


    def color_picker_dismiss(self,inst):
        '''
        '''
        self.color_picker.dismiss()


    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        '''
        Called when a gradient image is clicked.
        '''
        

    def dialog_color_picker_open(self):
        '''
        popup dialog used to edit a field (e.g., project name)
        '''
        self.color_picker_dialog = MDDialog(
            title='Click a color to select',
            text='Click "More Colors" to select a different color',
            type="custom",
            pos_hint = {'center_x': .5, 'top': .9},
            content_cls=ColorPickerDialog(),
            )
        
        self.color_picker_dialog.open()
        
        
    def dialog_color_picker_save(self, inst):
        '''
        save the color selected in the color picker dialog
        '''
        self.update_color(inst.md_bg_color)
        self.color_picker_dialog.dismiss()
