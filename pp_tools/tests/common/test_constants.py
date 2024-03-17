import os
import unittest
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.constants import BASE_PATH
from pp_tools.common.constants import COMMON_PATH


class TestConstants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """called once, before any test"""
        pass
        
    @classmethod
    def tearDownClass(cls):
        """called once, after all tests, if setUpClass successful"""
        pass
    
    def setUp(self):
        """called multiple times, before every test method"""
        pass
    
    def tearDown(self):
        """called multiple times, after every test method"""
        pass

    def test_base_path(self):
        flag = False
        if os.path.isdir(BASE_PATH):
            flag = True
        self.assertTrue(flag)
    
    def test_common_path(self):
        flag = False
        if os.path.isdir(COMMON_PATH):
            flag = True
        self.assertTrue(flag)


if __name__ == '__main__':
    unittest.main()
