# -*- coding: utf-8 -*-
import unittest
if __name__ == '__main_-':
    import sys
    sys.path.append("../")
import os

from ml.io.storage import Storage
from ml.conf.configurator import GLOBAL_CONFIGURATION

def setUpModule():
    """
    called once, before anything else in this module
    """
    print("Creating test data")
    
def tearDownModule():
    """called once, after everything else in this module"""
    print("Deleting Test Data")

class TestStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """called once, before any test"""
        print("In setUpClass()...")
        
    @classmethod
    def tearDownClass(cls):
        """called once, after all tests, if setUpClass successful"""
        print("In tearDownClass()...")
    
    def setUp(self):
        """called multiple times, before every test method"""
        print("\nIn setUp()...")
    
    def tearDown(self):
        """called multiple times, after every test method"""
        print("In tearDown()...")

    def test01(self):
        storage = Storage()
        print(storage.uuid_str)
        self.assertTrue(True)
    
    def test02(self):
        self.assertTrue(True)
    
    def test03(self):
        self.assertTrue(True)
        
    def test_space_available(self):
        stat = os.statvfs(GLOBAL_CONFIGURATION["PATH"])
        free_space_mb = (stat.f_bavail * stat.f_frsize) / 1048576
        free_space_gb = free_space_mb / 1024
        # print("Insuficient space available {0:,.2f} GB".format(free_space_gb))
        message = "Insuficient space, available {0:,.2f} GB required {1:,.2f} GB".format(free_space_gb, GLOBAL_CONFIGURATION["minimum_space"])
        print(message)
        self.assertGreater(free_space_gb, GLOBAL_CONFIGURATION["minimum_space"], message)

if __name__ == '__main__':
    unittest.main()

