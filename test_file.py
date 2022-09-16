

class DatabaseClient(object):
    pass            
    

class DatabaseInterface(object):        
    '''Object Description'''
        
    def __init__(self, database_name: str,  client: DatabaseClient,  delete_all_values: None,  auto_increment_id: None) -> None:
        self.database_name = database_name
        self.client = client
        self.delete_all_values = delete_all_values
        self.auto_increment_id = auto_increment_id
    
    def create_tables(self) -> None:
        '''signature description'''
        pass
    
    def read_tables(self) -> str:
        '''signature description'''
        pass
    
    def update_tables(self) -> None:
        '''signature description'''
        pass
    
    def delete_tables(self) -> None:
        '''signature description'''
        pass
    
    def create_values(self) -> None:
        '''signature description'''
        pass
    
    def read_all_values(self) -> str:
        '''signature description'''
        pass
    
    def read_value(self) -> str:
        '''signature description'''
        pass
    
    def update_value(self) -> None:
        '''signature description'''
        pass
    
    def delete_value(self) -> None:
        '''signature description'''
        pass
    
    def read_tables(self) -> str:
        '''signature description'''
        pass
import DatabaseClient
import unittest
import DatabaseInterface

print("Testing:" + DatabaseInterface.__doc__)
        

class Test_DatabaseInterface(unittest.TestCase):        
    '''Object Description'''
        
    def setUp(self, database_name: str,  client: DatabaseClient,  delete_all_values: None,  auto_increment_id: None) -> None:
        self.databaseinterface = DatabaseInterface()
        self.client = client
        
        self.delete_all_values = delete_all_values
        
        self.auto_increment_id = auto_increment_id
        
    
    def test_create_tables(self) -> None:
        '''signature description'''
        pass
    
    def test_read_tables(self) -> str:
        '''signature description'''
        pass
    
    def test_update_tables(self) -> None:
        '''signature description'''
        pass
    
    def test_delete_tables(self) -> None:
        '''signature description'''
        pass
    
    def test_create_values(self) -> None:
        '''signature description'''
        pass
    
    def test_read_all_values(self) -> str:
        '''signature description'''
        pass
    
    def test_read_value(self) -> str:
        '''signature description'''
        pass
    
    def test_update_value(self) -> None:
        '''signature description'''
        pass
    
    def test_delete_value(self) -> None:
        '''signature description'''
        pass
    
    def test_read_tables(self) -> str:
        '''signature description'''
        pass
    def tearDown(self):
        pass
        
if __name__ == "__main__":
    unittest.main()
        