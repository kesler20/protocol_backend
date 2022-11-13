
import unittest
import Completed

print("Testing:" + Completed.__doc__)
        

class Test_Completed(unittest.TestCase):        
    '''Object Description'''
        
    def setUp(self, Valid: None) -> None:
        self.completed = Completed()
    
    def test_this(self) -> None:
        '''signature description'''
        pass
    def tearDown(self):
        pass
        
if __name__ == "__main__":
    unittest.main()
        