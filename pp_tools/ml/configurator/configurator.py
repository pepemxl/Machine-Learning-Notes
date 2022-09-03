#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 13:51:16 2022

@author: Jose Alonzo

Only this class should be able to modify global configuration
in order to prevent accidental modifications
"""

from types import MappingProxyType
import platform
import os


__node_configuration = {
    "version": 0, 
    "subversion": 1,
    "node": platform.node(),
    "processor": platform.processor(),
    "system": platform.system(),
    "PATH": os.path.join(os.path.expanduser('~'), 'FSS')
}

GLOBAL_CONFIGURATION = MappingProxyType(__node_configuration)

if not os.path.isdir(GLOBAL_CONFIGURATION["PATH"]):
    print("Creating folder {0}".format(GLOBAL_CONFIGURATION["PATH"]))
    os.mkdir(GLOBAL_CONFIGURATION["PATH"])


if __name__=='__main__':
    print(GLOBAL_CONFIGURATION)