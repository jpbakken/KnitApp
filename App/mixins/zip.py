#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 10:20:10 2022

@author: jpbakken
"""
import zipfile
from datetime import datetime
import os


# =============================================================================
# create a compressed backup and save to projects backup
# =============================================================================
class Zip():
    data_dir = None
    wk_project_name = None
    backup_dirname = None
    
    # compress file function
    def zip_file(self,file_path):
        compress_file = zipfile.ZipFile(file_path + '.zip', 'w')
        compress_file.write(file_path, compress_type=zipfile.ZIP_DEFLATED)
        compress_file.close()
    
    
    # Declare the function to return all file paths of the particular directory
    def zip_get_file_paths(self,dir_name):
        # setup file paths variable
        file_paths = []
    
        # Read all directory, subdirectories and file lists
        for root, directories, files in os.walk(dir_name):
            for filename in files:
                # Create the full file path by using os module.
                file_path = os.path.join(root, filename)
                file_paths.append(file_path)
    
        # return all paths
        return file_paths
    
    
    def zip_dir(self,dir_path, file_paths):
        # write files and folders to a zipfile
        compress_dir = zipfile.ZipFile(dir_path + '.zip', 'w')
        with compress_dir:
            # write each file separately
            for file in file_paths:
                compress_dir.write(file)

    def zip_project(self):
        '''
        '''
        os.chdir(self.data_dir)
        
        path = self.wk_project_name
        files_path = self.zip_get_file_paths(path)

        self.zip_dir(path, files_path)
        
        file_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = self.wk_project_name + '.zip'
        
        self.zip_filename = self.wk_project_name \
            + '|' + file_time + '|.zip'
        os.rename(zip_filename,self.zip_filename)

        
        self.backup_path = os.path.join(self.backup_dirname,
                                        self.wk_project_name, 
                                        self.zip_filename)
