# -*- coding: utf-8 -*-
"""
@author: Jose Alonzo
@email: pepemxl@gmail.com
Machine Learning projects are scalable through data pipelines, however resources for development are often an issue in scaled systems, 
it don't make sense for relative small datasets being pulled thousands of times, these petitions are waiting in a queue of jobs for a large time,
while the current process takes a few minutes and a small machine. That's where a local/dev environment will become handy.

We need a handler of data in local/dev environments and monitors to handle this data and its transformations, as it will be working with a 
production environment, however, it will be a semi offline service

It will support and manage the production and consumption of data for a variety of business purposes, including publicly reported metrics 
(e.g., monthly or daily active users), recommendations, A/B testing, ads targeting, etc. 

Common enterprise systems run some of the largest Hadoop clusters in the world, on the Hadoop Distributed File System (HDFS), where ETL (Extract, Transform, and Load), 
data science and analytics, while Presto is employed for interactive querying. Vertica (or MySQL) is used for querying commonly aggregated datasets, and for Tableau dashboards. Manhattan is our distributed database used to serve live real-time traffic.

- Mechanisms to audit projects
    - Log state of current pipeline
    - Be able to reproduce pipeline and every expensive step
    - 
- Consider time of retention of data
    - Different types of data is under different restrictions of retention
    
This storage Data Access Layer (DAL) have the following goals:

- Data Discovery: 
    - how can we find datasets that are the most important? 
    - who owns these datasets? 
    - what are their semantics and other relevant metadata?
- Data Auditing: 
    - who creates or consumes these datasets, 
    - how are they created, 
    - what are their dependencies and their service-level agreements (SLAs), 
    - what are their alerting rules and are they consistent with their dependencies, and 
    - how is the lifecycle of the datasets managed?
- Data Abstraction: 
    - what does the data represent logically and what is its physical representation, 
    - where is it located, where is it replicated to, and what is the format?
- Data Consumption: 
    - how can the datasets be consumed interchangeably by various clients/devservers?
"""

from enum import Enum
import os
import platform

import pandas as pd
import datetime
import uuid
from collections import namedtuple
from typing import Optional



class StorageType(Enum):
    """ Enumeration of storage types

    Args:
        Enum (NONE): Not defined
        Enum (INPUT): Only read input storage
        Enum (OUTPUR): Output Storage  readeable/writeable
    """    
    NONE = 0
    INPUT = 1
    OUTPUT = 2

class RetentionPolicy(Enum):
    """ Enumeration of Retention Policies.

    Args:
        Enum (NONE): Not defined
        Enum (DAY): 1 day retention
        Enum (WEEK): 7 days retention
        Enum (MONTH): 30 days retention
        Enum (HALF): 180 days retention
        Enum (YEAR): 365 days retention
        Enum (FIVE_YEARS): 365 days retention
        Enum (TEN_YEARS): 365 days retention
        Enum (YEAR): 365 days retention
    """
    NONE = 0
    DAY = 1
    WEEK = 7
    MONTH = 30 # 30 DAYS
    HALF = 180 # 180 DAYS
    YEAR = 365 # 365 DAYS
    FIVE_YEARS = 1825 
    TEN_YEARS = 3650
    NEVER = 65535 # 65535 DAYS
    
    policies_descriptions = {
        0: 'Policy not defined',
        1: 'Storage content should be reset each day'
    }

class StorageStatus(Enum):
    """ Current Storage Status

    Args:
        Enum (NONE): Not defined
        Enum (CREATE): Storage Created
        Enum (REPLACE): Storage Replaced
        Enum (UPDATE): Storage Updated
        Enum (DELETE): Storage Deleted
    """    
    NONE = 0
    CREATE = 1
    REPLACE = 2
    UPDATE = 3
    DELETE = 4

class StoragePlaceHolder(Enum):
    """ Storage place holder system.

    Args:
        Enum (PICKLE): Use standar built in pickle storage
    """    
    LOCAL = 0
    HDFS = 1
    S3 = 2
    CASSANDRA = 3
    HIVE = 4
    CSV = 5
    PARQUET = 6
    JSON = 7
    BLOB = 8
    KAFKA = 9
    RDBMS = 10
    PICKLE = 11

class Storage:
    
    def __init__(self, _name:Optional[str]=None, _uuid:Optional[str]=None):
        self.name = _name
        self.uuid = _uuid
        if not self.uuid:
            self.generate_uuid()
        else:
            self.convert_uuid_to_str()
        self.path = None
        self.status = StorageStatus.NONE
        self.storage_place_holder = StoragePlaceHolder.LOCAL
        self.rentetion_policy = RetentionPolicy.NONE
        self.storage_type = StorageType.NONE
        #self.ds = datetime.datetime.
        #self.ds
    
    def generate_uuid(self):
        self.uuid = uuid.uuid4()
        self.convert_uuid_to_str()
    
    def convert_uuid_to_str(self):
        if isinstance(self.uuid, uuid.uuid4().__class__):
            self.uuid_str = str(self.uuid.hex)
    
    def get_uuid(self):
        return self.uuid
    
    def get_uuid_str(self):
        return self.uuid_str
    
    def set_uuid(self):
        pass



class Input(Storage):
    
    def __init__(self):
        
        super().__init__()


class Output(Storage):
    
    def __init__(self):
        self.status = 0




if __name__ == '__main__':
    storage = Input()
    print(storage.get_uuid())
    print(storage.get_uuid_str())

