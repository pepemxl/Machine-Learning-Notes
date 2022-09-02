# -*- coding: utf-8 -*-
import unittest

import sys
sys.path.append("../")

from ml.io.storage import Storage

class TestStorage(unittest.TestCase):
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

