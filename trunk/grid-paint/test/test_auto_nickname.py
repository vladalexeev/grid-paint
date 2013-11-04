'''
Created on 04.11.2013

@author: Vlad
'''

import unittest

from pages.common import auto_nickname

class Test (unittest.TestCase):
    def test_auto_nickname(self):
        self.assertEqual(auto_nickname('user'), 'user')
        self.assertEqual(auto_nickname('user@domain'), 'user@domain')
        self.assertEqual(auto_nickname('user@domain.'), 'user@domain.')
        self.assertEqual(auto_nickname('user@domain.com'), 'user@d...com')
        self.assertEqual(auto_nickname('user@sub.domain.com'), 'user@s...com')
    
    
if __name__ == "__main__":
    unittest.main()