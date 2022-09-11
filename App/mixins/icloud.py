#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 10:25:50 2022

@author: jpbakken
"""
from mixins.layout import EditFieldDialog
from mixins.layout import iCloudCredentialsDialog

import json

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from pyicloud import PyiCloudService
import threading
import os

# =============================================================================
# icloud drive functions
# =============================================================================


class iCloud():
    
    
    def icloud_thread_start(self,target):
        '''
        '''
        self.icloud_thread = threading.Thread(target=target)
        self.icloud_thread.start()
        self.icloud_thread.join()


    def icloud_read(self):
        '''
        '''
        cookie_directory = os.path.join(self.data_dir,'_cookies')        

        # create/refresh the connection to icloud
        self.icloud = PyiCloudService(self.apple_id,
                                      self.apple_password,
                                      cookie_directory=cookie_directory,
                                      )
        
    def icloud_auth(self):
        '''
        start icloud service with username and password
        
        return to do 2 factor authentication if session is untrusted
    
        if authenticated, process the icloud action
        '''
        
        self.icloud_read()
        
        # not trusted, break the thread and go through auth code steps
        if not self.icloud.is_trusted_session:
            return
        
        # create the app folder if needed
        if not self.app_name in self.icloud.drive.dir():
            self.icloud.drive.mkdir(self.app_name)        
            self.icloud_read()

        # process the icloud action
        else:
            if self.icloud_action == 'backup':
                self.icloud_backup()


    def dialog_icloud_auth(self):
        '''
        popup dialog used to enter authorization code
        '''
        self.edit_field_name = 'Authentication Code'
        self.edit_field_text = ''

        self.icloud_auth_dialog = MDDialog(
            title='Enter Code',
            type="custom",
            pos_hint = {'center_x': .5, 'top': .9},
            content_cls=EditFieldDialog(),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=self.dialog_icloud_auth_dismiss),
                MDFlatButton(
                    text="Save",
                    on_release=self.dialog_icloud_2f)])
        
        self.icloud_auth_dialog.open()


    def dialog_icloud_login(self):
        '''
        popup dialog used to save username and password
        '''
        self.edit_field_name = 'iCloud Authentication'
        self.edit_field_text = ''
        

        self.icloud_login_dialog = MDDialog(
            title='Log in with your Apple Id and password',
            type="custom",
            pos_hint = {'center_x': .5, 'top': .9},
            content_cls=iCloudCredentialsDialog(),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=self.dialog_icloud_login_dismiss),
                MDFlatButton(
                    text="Save",
                    on_release=self.dialog_icloud_login_save)])
        
        self.icloud_login_dialog.open()


    def dialog(self,
                title='Failed', 
                text='Verification failed. Please try again.'):
        
        MDDialog(title=title,
                  text=text,
                  pos_hint = {'center_x': .5, 'top': .9}).open()


    def dialog_icloud_auth_dismiss(self, inst):
        '''
        dismiss the dialog
        '''
        self.icloud_auth_dialog.dismiss()


    def dialog_icloud_login_dismiss(self, inst):
        '''
        dismiss the dialog
        '''
        self.icloud_login_dialog.dismiss()

        
    def dialog_icloud_login_save(self, inst):
        '''
        encrypt and save login details
        
        '''
        self.apple_id = self.icloud_login_dialog.content_cls.ids.apple_id.text
        self.apple_password = self.icloud_login_dialog.content_cls.ids.apple_password.text
        self.icloud_write_encrypted()

        self.icloud_login_dialog.dismiss()
        

        self.icloud_auth()        

        if self.icloud:
            if not self.icloud.is_trusted_session:
                self.dialog_icloud_auth()


    def icloud_write_encrypted(self):
        '''
        '''

        data = {"apple_id":self.apple_id,
                "apple_password": self.apple_password}
        
        # data_bytes = json.dumps(data).encode('utf-8')
        # encrypted = self.fernet.encrypt(data_bytes)
        # with open(self.encrypted_filepath, 'wb') as f:
        #     f.write(encrypted)

        with open(self.encrypted_filepath, 'w') as f:
            json.dump(data, f)

    def icloud_read_encrypted(self):
        '''
        '''
        if not os.path.exists(self.encrypted_filepath):
            self.apple_id = ''
            self.apple_password = ''
            self.icloud_write_encrypted()
        
        with open(self.encrypted_filepath, 'r') as f:
            data_dict = json.load(f)
        
        # with open(self.encrypted_filepath, 'rb') as f:
        #     data = f.read()
        # decrypted = self.fernet.decrypt(data)
        # data_dict = json.loads(decrypted.decode('utf8'))
    

        self.apple_id = data_dict['apple_id']
        self.apple_password = data_dict['apple_password']
    
            
            
        
    def dialog_icloud_2f(self, inst):
        '''
        use input from the dialog to do 2 factor authentication
        
        '''
        self.api_code = self.icloud_auth_dialog.content_cls.ids.edit_field.text

        result = self.icloud.validate_2fa_code(self.api_code)
        
        if not result:
            self.dialog()
    
        elif not self.icloud.is_trusted_session:
            self.dialog(
                text="Session is not trusted. Requesting trust...")    
            result = self.icloud.trust_session()
            
            if not result:
                self.dialog(
                    text="Failed to request trust. You will likely be prompted for the code again in the coming weeks")

        elif self.icloud_action == 'backup':
            
            self.dialog(title='Authenticated' ,
                        text='Proceeding with backup')
            

        self.dialog_icloud_auth_dismiss(inst)
        
        # try the backup again once authenticated
        if self.icloud_action == 'backup':
            self.project_backup()        
        
        
    def icloud_backup(self):
        '''
        '''        
        self.zip_project()
        
        app_dir = self.icloud.drive[self.app_name]
                
        if not self.wk_project_name in app_dir.dir():
            app_dir.mkdir(self.wk_project_name)
            self.icloud_read()
            app_dir = self.icloud.drive[self.app_name]

        project_dir = app_dir[self.wk_project_name]
        
        file = self.zip_filename
                    
        with open(file, 'rb') as f:
            project_dir.upload(f)
            
        os.rename(self.zip_filename,self.backup_path)

        self.project_del_local_backup()
        self.project_del_icloud_backup()


    def icloud_download(self, file):
        '''
        '''
