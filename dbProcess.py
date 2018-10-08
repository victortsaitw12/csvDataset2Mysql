#!/usr/bin/python

import pymysql.cursors 
import json
from dictToObject import DictToObject 

class SqlConnector(object):

    def __init__(self, config=None):
        if config is None:
            config = {
                'user': 'root',
                'password': '12345',
                'host': 'localhost',
                'db': 'repository',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            }
        self.cnx = pymysql.connect(**config)


    def insert(self, command, arg=[]):
        with self.cnx.cursor() as cur:
            cur.execute(command, arg)
        insert_id = self.cnx.insert_id()
        self.cnx.commit()
        return insert_id 


    def insertDataRow(self, table, row, features, folder_path):
        command = 'INSERT INTO ' + table + '(';
        values = ''
        for feature in features.toDict():
            command = command + feature + ','
            values = values + '"' + row[feature] + '",'
        command = command + 'full_path'
        values = values + '"' + folder_path + '"'
        command = command + ') VALUES(' + values + ')'
        return self.insert(command)


    def recordMetadata(self, metadata=None):
        ''' Record dataset '''
        dataset_id = self.insert2Dataset(DictToObject({
            'metadata': metadata.toJSON(),
            'name': metadata.dataset.name,
            'description': metadata.dataset.description
        }))
        if dataset_id <= 0:
            return []

        ''' Record Resource '''
        processed_resource = []
        for resource in metadata.dataset.resource:
            resource['dataset_id'] = dataset_id
            resource['table_name'] = metadata.dataset.name + '_' + resource['name']
            resource['creater'] = metadata.dataset.creater
            if isinstance(resource, dict):
                resource = DictToObject(resource)
            resource_id = self.processResource(resource)
            print('resource id: %s' % resource_id)
            if resource_id <= 0:
                continue
            processed_resource.append(resource)
        return processed_resource
            

    def processResource(self, resource=None):
        resource_id = self.insert2Resource(resource)
        if resource_id > 0:
            self.createTable(resource);
        return resource_id


    def createTable(self, resource=None):
        command='CREATE TABLE ' + resource.table_name + '(';
        length = len(resource.features.toDict())
        for feature, types in resource.features.toDict().items():
            command = command + feature + ' ' + types
            command = command + ','
        command = command + 'full_path varchar(255),'
        command = command + 'id int auto_increment primary key'
        command = command + ')';
        with self.cnx.cursor() as cur:
            cur.execute(command)
        self.cnx.commit()


    def checkResource(self, data=None):
        row = None
        with self.cnx.cursor() as cur:
            command='''SELECT * FROM resource
            WHERE dataset_id = %s AND name = %s
            '''
            cur.execute(command,
                (data.dataset_id, data.name))
            row = cur.fetchone()
        return (row is None)


    def insert2Resource(self, data=None):
        if self.checkResource(data) == False:
            return 0

        with self.cnx.cursor() as cur:
            command='''INSERT INTO resource(
                dataset_id, name, type, creater, table_name, format) VALUES(
                %s, %s, %s, %s, %s, %s
            )
            '''
            cur.execute(command, 
                (data.dataset_id, data.name, data.type,
                 data.creater, data.table_name, data.format))
        insert_id = self.cnx.insert_id()
        self.cnx.commit()
        return insert_id


    def checkDataset(self, data=None):
        row = None
        with self.cnx.cursor() as cur:
            command='''SELECT * FROM dataset
            WHERE name = %s
            '''
            cur.execute(command, (data.name))
            row = cur.fetchone()
        return (row is None)


    def insert2Dataset(self, data=None):
        if self.checkDataset(data) == False:
            return 0

        with self.cnx.cursor() as cur:
            command = '''INSERT INTO dataset(
              name, description, metadata) VALUES(
              %s, %s, %s
              )
            '''
            cur.execute(command,
                (data.name, data.description, data.metadata))
        insert_id = self.cnx.insert_id()
        self.cnx.commit()
        return insert_id


    def __del__(self):
        self.cnx.close()


if __name__ == '__main__':
    sql = SqlConnector()
    test_dataset = DictToObject({
      'name': 'whole_experiment_data',
      'dataset_id': 90
    })
    result = sql.checkResource(test_dataset)
    print(result)
