#!/usr/bin/python

import scipy.io as sio

class MatProcess(object):

    def __init__(self, osProcess, sql,
                 features, table,
                 folders=[], files=[]):
                 
        print('init MatProcess')
        self.osProcess = osProcess
        self.sql = sql
        self.folders = folders
        self.files = files
        self.features = features
        self.table = table

    def readMat(self, path):
        datas = sio.loadmat(path)
        print(datas)
        #fe_time = datas['X118_FE_time'][:]
        #print(fe_time)

'''
    def saveToDatabase(self):
        for folder in self.folders:
            self.csvInFolderToSql(self.table, folder, self.features)

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
'''

if __name__ == '__main__':
    mat = MatProcess(
      osProcess = 
      folders= [
          '/Users/victor.tsai/myPractice/data_repository/mat_src/12k_Drive_End_Bearing_Falut_Data'
      ]
    )

