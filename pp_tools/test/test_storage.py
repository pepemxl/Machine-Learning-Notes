# -*- coding: utf-8 -*-
import unittest

import sys
sys.path.append("../")

from ml.io.storage import Storage

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

if __name__ == '__main__':
    unittest.main()

