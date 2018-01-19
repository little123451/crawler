#!/usr/bin/env python
# coding:utf-8

import json
import api_sdk
import logger
log = logger.getLogger('DataModel','INFO')

class DataModel:
    def __init__(self):
        self.data = {}
        self.id = ''
        pass

    def set(self, key, value):
        self.data[key] = value
        pass

    def set_id(self, object_id):
        self.set('id', object_id)
        pass

    def get(self, key):
        if (key in self.data):
            return self.data[key]
        return None
        pass

    def dump(self, level='DEBUG'):
        if (level == 'DEBUG') : log.debug(json.dumps(self.data))
        if (level == 'INFO') : log.info(json.dumps(self.data))
        if (level == 'WARN') : log.warn(json.dumps(self.data))
        if (level == 'ERROR') : log.error(json.dumps(self.data))
        pass
    
    def save(self, type = None):
        api_sdk.save(self.data, type)
        pass
