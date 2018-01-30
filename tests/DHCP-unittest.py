import unittest
from DHCP import DHCP

class TestDHCPMethods(unittest.TestCase):
        def test_mac(self):
            self.assertEqual(DHCP().unittest_matchMac(), "34:e6:d7:43:c9:6c")

        def test_suffix(self):
            self.assertEqual(DHCP().unittest_removeSuffix(), "will")

        def test_dash(self):
            self.assertEqual(DHCP().unittest_handleDashSuffix(), "will")

        def test_multi(self):
            self.assertEqual(DHCP().unittest_handleMultiName(), "Will")

            
if __name__ == '__main__':
    unittest.main()
