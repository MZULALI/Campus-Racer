import unittest
from hardware.multiplexer import Multiplexer

class TestMultiplexer(unittest.TestCase):
    def setUp(self):
        config = {
            'address': 0x70,
            'control_pins': {
                'sel': [17, 27, 22]
            }
        }
        self.multiplexer = Multiplexer(config)
    
    def test_select_channel(self):
        try:
            self.multiplexer.select_channel(0)
            self.multiplexer.select_channel(1)
            self.multiplexer.select_channel(2)
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"select_channel raised an exception {e}")
    
    def tearDown(self):
        self.multiplexer.cleanup()

if __name__ == '__main__':
    unittest.main()
