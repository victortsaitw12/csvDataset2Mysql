#!/usr/bin/python

import json

class DictToObject(object):

    def __init__(self, a_dict):
        self.__dict__.update(a_dict)
        for k, v in a_dict.items():
            if isinstance(v, dict):
                self.__dict__[k] = DictToObject(v)
            
    def show(self):
        print('showshowshow')

    def toJSON(self):
        print('toJSON')
        a_dict = self.__dict__.copy()
        for k, v in self.__dict__.items():
            if isinstance(v, DictToObject):
                a_dict[k] = v.toJSON()
        result = json.dumps(a_dict)
        print(result)
        return result

    def toDict(self):
        print('toDict')
        a_dict = self.__dict__.copy()
        for k, v in self.__dict__.items():
            if isinstance(v, DictToObject):
                a_dict[k] = v.__dict__.copy()
        result = a_dict
        print(result)
        return result


def transfer(a_dict):
    return DictToObject(a_dict)


if __name__ == '__main__':
    a = transfer({'name': 'victor'})
    print(a.toJSON())
    b = transfer({'name': 'victor', 'money':{'rmb': 400, 'ntd': 500}})
    print(b.toJSON())
    c = transfer({'name': 'victor', 'money':{'rmb': 400, 'ntd': 500}, 'skill':['python', 'c++']})
    print(c.toJSON())
    c = transfer({'name': 'victor', 'money':{'rmb': 400, 'ntd': {'one': 5, 'five':100}}, 'skill':['python', 'c++']})
    print(c.toJSON())
