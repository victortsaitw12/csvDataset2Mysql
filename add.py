#!/usr/bin/python

import sys
import os
import dictToObject
from dbProcess import SqlConnector
from fileProcess import FileProcess
from csvProcess import CSVProcess

def main(argv):
    src = os.path.dirname(argv[0])
    osProcess = FileProcess()
    sql = SqlConnector()
    metadata = osProcess.loadMetadata(src)
    osProcess.saveDataset(metadata)
    processed_resource = sql.recordMetadata(metadata)
    for resource in processed_resource:
        if 'folders' in resource.toDict() and 'csv' == resource.format:
            CSVProcess(
                osProcess, sql, resource.features,
                resource.table_name, folders=resource.folders
            ).saveToDatabase()

        elif 'files' in resource.toDict() and 'csv' == resource.format:
            csv = CSVProcess(
                osProcess, sql, resource.features,
                resource.table_name, files=resource.files
            ).saveToDatabase()
        
if __name__ == "__main__":
    main(sys.argv[1:])
