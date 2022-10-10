
import unittest
from file import Food, Meal, Diet
print("Testing:" + Food.__doc__)
        

class Test_Food(unittest.TestCase):        
    '''
    Food the unit created by te user which is a dictionary containing the following values
    self['Name'] = name
    self['Cost (£)'] = cost
    self['protein (g/amount)'] = protein
    self['calories (g/amount)'] = calories
    
    '''
        
    def setUp(self, name: str,  cost: float,  protein: float,  calories: int) -> None:
        self.food = Food()
        self.cost = cost
        
        self.protein = protein
        
        self.calories = calories
        
    def tearDown(self):
        pass
        

class Test_Meal(unittest.TestCase):        
    '''
    Meal, a meal is a collection of foods which has also a name, this has a property of total which
    represents a dictionary of the following key value pairs
    self['Cost (£)'] = cost
    self['protein (g/amount)'] = protein
    self['calories (g/amount)'] = calories
    '''
        
    def setUp(self) -> None:
        self.meal = Meal()
        
    
    def test_calculate_total(self) -> list:
        '''signature description'''
        pass
    def tearDown(self):
        pass
        

class Test_Diet(unittest.TestCase):        
    '''- Diet, a diet is a collection of meals which has a day of the week id, therefore there can only be 7 diets in a week'''
        
    def setUp(self) -> None:
        self.diet = Diet()
        
    def tearDown(self):
        pass
        
if __name__ == "__main__":
    unittest.main()
        