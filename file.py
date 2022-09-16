

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