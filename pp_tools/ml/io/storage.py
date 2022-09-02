# -*- coding: utf-8 -*-
"""
@author: Jose Alonzo
Machine Learning projects are scalable through data pipelines, 
however resources for development are an issue in scaled systems, 
it don't make sense for small datasets being pulled thousands of times, 
these petitions are waiting in a queue of jobs. 
That's where a local/dev environment will become handy.

We need a handler of data in local/dev environments and monitors to handle
this data and its transformations.

- Mechanisms to audit projects
    - Log state of current pipeline
    - Be able to reproduce pipeline and every expensive step
    - 
- Consider time of retention of data
    - Different types of data is under different restrictions of retention
"""

from enum import Enum
import os
import platform

import pandas as pd
import datetime
import uuid




class StorageType(Enum):
    NONE = 0 # No defined
    INPUT = 1
    OUTPUT = 2

class RetentionPolicy(Enum):
    NONE = 0
    DAY = 1
    WEEK = 2
    MONTH = 3 # 30 DAYS
    HALF = 4 # 180 DAYS
    YEAR = 5 # 365 DAYS

class StorageStatus(Enum):
    NONE = 0
    CREATE = 1
    REPLACE = 2
    UPDATE = 3
    DELETE = 4

class Storage:
    
    def __init__(self):
        self.name = None
        self.uiid = None
        self.uiid_str = None
        self.path = None
        self.status = StorageStatus.NONE
        self.rentetion_policy = RetentionPolicy.NONE
        self.storage_type = StorageType.NONE
        self.generate_uuid()
    
    def generate_uuid(self):
        self.uiid = uuid.uuid4()
        self.uuid_str = str(uuid.uuid4().hex)
    
    def set_uuid(self):
        pass



class Input(Storage):
    
    def __init__(self):
        pass


class Output(Storage):
    
    def __init__(self):
        self.status = 0




if __name__ == '__main__':
    pass




