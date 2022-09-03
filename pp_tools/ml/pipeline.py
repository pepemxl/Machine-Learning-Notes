#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 01:00:32 2022

@author: pepe
"""

from enum import Enum

from collections import defaultdict
dd = defaultdict(list)

# Accessing a missing key creates it and
# initializes it using the default factory,
# i.e. list() in this example:
dd["features"].append("1")
dd["fields"].append("1")
dd["labels"].append("1")


class ETL(Enum):
    """
    Extract: The first stage of the ETL process retrieves data from 
    its source system into a single format appropriate for transformation 
    processing. 
    Transform: This is the stage when a set of rules are applied to the extracted 
    data to ensure data quality and accessibility and to prepare it for the final 
    stage in the process.
    Load. This stage is when the extracted and transformed data is loaded 
    into the end target source of a data warehouse, 
    data hub or data lake structure.
    """
    EXTRACT = 0
    TRANFORM = 1
    LOAD = 2
    

class EDA(Enum):
    EXTRACT = 0
    TRANFORM = 1
    LOAD = 2