#!/usr/bin/python

import csv

class CSVProcess(object):
    def __init__(self, osProcess, sql,
                 features, table,
                 folders=[], files=[]):
        print('init CSVProcess')
        self.osProcess = osProcess
        self.sql = sql
        self.folders = folders
        self.files = files
        self.features = features
        self.table = table

    def saveToDatabase(self):
        '''COPY Dataset in Folder to DB'''
        for folder in self.folders:
            self.csvInFolderToSql(self.table, folder, self.features)

        '''COPY Dataset to DB'''
        for path in self.files:
            self.csvToSql(self.table, path, self.features)


    def csvInFolderToSql(self, table, path, features):
        files = self.osProcess.getFilesInFolder(path)
        for file_long in files:
            self.csvToSql(table, file_long, features)


    def csvToSql(self, table, path, features):
        csvReader = csv.DictReader(open(path, 'r'))
        for row in csvReader:
            self.sql.insertDataRow(table, row, features, path)

if __name__ == '__main__':
    print('hi')
