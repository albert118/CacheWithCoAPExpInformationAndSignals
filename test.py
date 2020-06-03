__doc__ = "SetUp test for the info and signals experiment."
__author__ = "Albert Ferguson"

import unittest



class Tests(unittest.TestCase):
    
    def setUp(self):
        self.proxy_address = ("127.0.0.1", 5683)
