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
import psutil
import shutil

import logging
from omegaconf import DictConfig, OmegaConf
import hydra
from typing import Optional
from ctypes import Structure, c_int32, c_uint64, sizeof, byref, windll

class MemoryStatusEx(Structure):
    _fields_ = [
        ('length', c_int32),
        ('memoryLoad', c_int32),
        ('totalPhys', c_uint64),
        ('availPhys', c_uint64),
        ('totalPageFile', c_uint64),
        ('availPageFile', c_uint64),
        ('totalVirtual', c_uint64),
        ('availVirtual', c_uint64),
        ('availExtendedVirtual', c_uint64)]
    def __init__(self):
        self.length = sizeof(self)

log = logging.getLogger(__name__)


def compute_memory()->Optional[float]:
    """ Getting all memory using os.popen()
        It will be RAM + SWAP in case of linux
    """
    log.info("Computing node memory available")
    pct_memory = None
    used_memory = None
    free_memory = None
    total_memory = None
    if platform == "linux" or platform == "linux2":
        # linux
        total_memory, used_memory, free_memory = map(
            int, 
            os.popen('free -t -m').readlines()[-1].split()[1:]
        )
        print(used_memory, free_memory, total_memory)
        print(used_memory/1024, free_memory/1024, total_memory/1024)
        pct_memory = round((used_memory/total_memory) * 100, 2)
    elif platform == "darwin":
        # OS X
        total_memory, used_memory, free_memory = map(
            int, 
            os.popen('free -t -m').readlines()[-1].split()[1:]
        )
        pct_memory = round((used_memory/total_memory) * 100, 2)
    elif platform == "win32":
        # Windows
        m = MemoryStatusEx()
        assert windll.kernel32.GlobalMemoryStatusEx(byref(m))
        print('You have %0.2f GiB of RAM installed' % (m.totalPhys / (1024.)**3))
    
  
    # Memory usage
    #print("RAM memory % used:", round((used_memory/total_memory) * 100, 2))
    
    return pct_memory


# DEFAULT_ARGS = {
#     "owner": "pepe",
#     "depends_on_past": False,
#     "start_date": datetime.datetime(2022, 08, 7),
#     "email": ["pepemxl@yahoo.com.mx"],
#     "email_on_failure": False,
#     "email_on_retry": False,
# }

__node_configuration = {
    "version": 0, 
    "subversion": 1,
    "node": platform.node(),
    "type_processor": platform.processor(),
    "number_cpu": os.cpu_count(),
    "pct_ram":psutil.virtual_memory()[2],
    "pct_ram2":compute_memory(),
    "system": platform.system(),
    "PATH": os.path.join(os.path.expanduser('~'), 'FSS')
}

@hydra.main(version_base=None, config_path='.', config_name='config')
def setup_configuration(cfg: DictConfig) -> None:
    # print(OmegaConf.to_yaml(cfg))
    global __node_configuration
    for key_ in cfg.keys():
        __node_configuration[key_] = cfg[key_]

setup_configuration()
GLOBAL_CONFIGURATION = MappingProxyType(__node_configuration)

if not os.path.isdir(GLOBAL_CONFIGURATION["PATH"]):
    print("Creating folder {0}".format(GLOBAL_CONFIGURATION["PATH"]))
    os.mkdir(GLOBAL_CONFIGURATION["PATH"])

stat = shutil.disk_usage(GLOBAL_CONFIGURATION["PATH"])
__node_configuration["rom_total"] = round(stat.total/(1024*1024*1024),2)
__node_configuration["rom_used"] = round(stat.used/(1024*1024*1024),2)
__node_configuration["rom_free"] = round(stat.free/(1024*1024*1024),2)


if __name__=='__main__':
    print(GLOBAL_CONFIGURATION)
