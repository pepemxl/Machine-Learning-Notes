import os
import unittest
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.environment_variables import test_logger
from pp_tools.common.environment_variables2 import test_logger2


class TestLogger(unittest.TestCase):
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
        test_logger()
        test_logger2()
        self.assertLogs()


if __name__ == '__main__':
    unittest.main()
