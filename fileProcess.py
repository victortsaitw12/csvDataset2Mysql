#!/usr/bin/python

import yaml
import os
import dictToObject
import shutil
import re

class FileProcess(object):
    def __init__(self):
        print('init FileProcess')

    def makeDestPath(self, metadata):
        return os.path.dirname('./history/rawData/%s/' % 
            metadata.dataset.name)

    def getFilesInFolder(self, path):
        file_pathes = []
        for root, dirs, files in os.walk(path):
            for file_path in files:
                file_long = os.path.join(root, file_path)
                file_pathes.append(file_long)
        return sorted(file_pathes)

    def saveDataset(self, metadata):
        '''Create Saving Folder'''
        folder = self.makeDestPath(metadata)
        self.createFolder(folder)
        '''Save Dataset'''
        for resource in metadata.dataset.resource:
            self.processResource(metadata, resource)

    def createFolder(self, folder):
        '''Create folder'''
        try:
            os.makedirs(folder)
        except Exception as ex:
            print(ex)

    def loadMetadata(self, src):
        metadata = {}
        with open(src + '/metadata.yaml' , 'r') as stream:
            try:
                metadata = yaml.load(stream)
            except yaml.YAMLError as ex:
                print(ex)
        metadata = dictToObject.transfer(metadata)
        return metadata

    def copyFileToDest(self, files, dest_folder):
        files = [file_name for file_name in files 
                 if os.path.isfile(file_name)]
        for file_path in files:
            if os.path.isfile(file_path):
                shutil.copy(file_path, dest_folder)

    def copyFolderToDest(self, folders, dest_folder):
        for folder_path in folders:
            new_dest_folder = os.path.join(dest_folder, os.path.basename(folder_path))
            self.createFolder(new_dest_folder)
            files = [os.path.join(folder_path, file_name) for 
                     file_name in os.listdir(folder_path)]
            self.copyFileToDest(files, new_dest_folder)

    def processResource(self, metadata, resource):
        '''cp file to dest folder'''
        folder = self.makeDestPath(metadata)
        if 'files' in resource:
            self.copyFileToDest(resource['files'], folder)

        if 'folders' in resource:
            self.copyFolderToDest(resource['folders'], folder)


if __name__ == '__main__':
    osProcess = FileProcess()
    files = osProcess.getFilesInFolder('history/rawData/dataset_test_name/training')
    print(files)
