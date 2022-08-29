
class Client(object):
    pass            
    
    
class SubscriptionModel(object):
    pass            
    
    
class BuiltClassName(object):        
    '''This is a class which is built using the ClassBuilder'''
        
    def __init__(self, client: Client,  subscription: SubscriptionModel,  status: str) -> None:
        self.client = client
        self.subscription = subscription
        self.status = status
    
    def foo(self) -> str:
        '''this is the description of foo'''
        pass
    
    def fizz(self) -> str:
        '''this is the description of fizz'''
        pass
    
    def buzz(self) -> int:
        '''this is the description of buzz'''
        pass