#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:56:59 2022

@author: jpbakken
"""
import kv
from itertools import compress
from kivy.lang import Builder
# from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.list import MDList
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton
# from kivymd.uix.dialog import MDDialog


class Knit():
    
# =============================================================================
# substep fuctions used while knitting
# =============================================================================
    def calc_substeps(self):
        '''
        '''
               
        self.wk_substeps = []
        
        for idx, step in enumerate(self.wk_piece):
            StepRow = step['StartRow']
            HowOften = step['HowOften']
            HowManyTimes = step['HowManyTimes']
            Code = step['Code']
            Action = step['Action']
            FontColor = step['FontColor']
            CodeStepNum = 1
            for substep in range(HowManyTimes):
                self.wk_substeps.append({'StepRow': StepRow,
                                 'Code': Code,
                                 'Action': Action,
                                 'FontColor': FontColor,
                                 'CodeStepNum': CodeStepNum,
                                 'HowManyTimes': HowManyTimes
                                 })
                
                # increment to next row to add
                StepRow =  StepRow + HowOften
                CodeStepNum += 1

        self.get_min_max_knit_row()
        
        self.write_wk_substeps()

    def get_min_max_knit_row(self):
        '''
        '''
        
        self.wk_piece_in_progress['StartRow'] = 999
        self.wk_piece_in_progress['EndRow'] = 0
        
        for step in self.wk_substeps:
            if step['StepRow'] < self.wk_piece_in_progress['StartRow']:
                self.wk_piece_in_progress['StartRow'] = step['StepRow']
            
            if step['StepRow'] > self.wk_piece_in_progress['EndRow']:
                self.wk_piece_in_progress['EndRow'] = step['StepRow']
           
                
        # start = [step['StepRow'] for step in steps if step['StepRow'] < start]
        # end = [step['StepRow'] for step in steps if step['StepRow'] > end]
        

    def get_current_substeps(self):
                
        current_substeps = [
            sub['StepRow'] == self.knit_step_row for sub in self.wk_substeps]
        
        self.step_row_substeps = list(compress(self.wk_substeps,
                                     current_substeps))


    def knit_piece_build(self):
        '''
        '''
        self.screen_name =  self.PieceKnitScreenName

        # show and clear anything left in the main layout
        self.clear_layout()
        
        self.menu_build(self.piece_knit_menu_labels) 

        # get or create work substeps and row
        self.get_wk_substeps()
        
        self.knit_piece_content_build()
        self.knit_piece_button_build()

        
    def knit_piece_content_build(self):
        
        self.write_wk_step_in_progress()
        
        self.widget_visible(self.root.ids.content_main)

        self.get_current_substeps()
        
        # build the list of pieces
        mdlist = MDList()        
        mdlist.add_widget(TwoLineListItem(disabled=True))
        # iterate through items and build the scroll list
        for i in self.step_row_substeps:
            
            self.root.ids.header.text = '{0} Row Number {1}'.format(
                self.wk_piece_name,
                i['StepRow'])
            
            mdlist.add_widget(
                TwoLineListItem(
                    text="{}".format(i['Action']),
                    secondary_text='{0}: {1} of {2} times'.format(
                        i['Code'],
                        i['CodeStepNum'],
                        i['HowManyTimes']),
                    secondary_theme_text_color = 'Custom',
                    secondary_text_color = [0,0,0,1],
                    secondary_font_style = 'Caption',
                    bg_color=i['FontColor'],
                    theme_text_color='Custom',
                    on_release=self.knit_piece_next_step)
                )
                        
        # add list to the scroll view
        scroll = ScrollView()
        scroll.add_widget(mdlist)

        # add widget to the content area
        self.root.ids.content_main.add_widget(scroll) 


    def knit_piece_button_build(self):
        # show and clear anything left in the widget
        self.widget_visible(self.root.ids.content_col)

        scroll = Builder.load_string(kv.scroll_list_widget)  
        mdlist = scroll.ids.mdlist
        
        for button in self.piece_knit_button_labels:
            
            # add a disabled item for spacer
            mdlist.add_widget(OneLineListItem(
                size_hint = (1, .25),
                disabled = True))
            
            # add the button
            button = MDRaisedButton(
                        text=button,
                        size_hint = (1,.8),
                        on_release = self.knit_piece_button_release,
                        )
                    
            mdlist.add_widget(button)
        
        self.root.ids.content_col.add_widget(scroll)


    def knit_piece_button_release(self, instance):
        '''
        '''
        if instance.text == self.piece_knit_button_previous:
            self.knit_piece_previous_step()
            
        elif instance.text == self.piece_knit_button_jump:
            self.piece_knit_jump_to_step()
            
        elif instance.text == self.piece_knit_button_next:
            self.knit_piece_next_step()
            
            
    def knit_piece_next_step(self, inst=None):
        '''
        advance to the next step
        '''
        self.knit_step_row += 1
        
        if self.knit_step_row > self.wk_piece_in_progress['EndRow']:
            self.dialog_knit_piece_reset()
            
        else:
            self.knit_piece_content_build()

    def knit_piece_previous_step(self, inst=None):
        '''
        
        '''
        # do not move steps into negative numbers
        if self.knit_step_row > 1:
            self.knit_step_row -= 1
            
        self.knit_piece_content_build()
    
    def knit_piece_reset(self, inst=None):
        '''
        reset knitting progress on a piece
        '''
        self.knit_piece_complete.dismiss()
        self.knit_step_row = 1
        self.write_wk_step_in_progress()
        self.knit_piece_build()


    def piece_knit_jump_to_step(self):
        '''
        '''
        self.edit_field_name = self.piece_knit_button_jump
        self.edit_field_check_list = [0]
        self.edit_field_text = str(self.knit_step_row)

        self.dialog_field_build()


