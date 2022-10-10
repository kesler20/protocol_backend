import unittest
import JsonDatabaseInterface

print("Testing:" + JsonDatabaseInterface.__doc__)
        

class Test_JsonDatabaseInterface(unittest.TestCase):        
    '''Interface which allows to store dictionaries as json'''
        
    def setUp(self, filename: str) -> None:
        self.jsondatabaseinterface = JsonDatabaseInterface()
    
    def test_createResource(self) -> None:
        '''signature description'''
        pass
    
    def test_readResource(self) -> dict:
        '''signature description'''
        pass
    
    def test_deleteResource(self) -> None:
        '''signature description'''
        pass
    
    def test_updateResource(self) -> None:
        '''signature description'''
        pass
    def tearDown(self):
        pass
        
if __name__ == "__main__":
    unittest.main()
        