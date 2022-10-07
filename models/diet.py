

class Nutrition(dict):

    def __init__(self):
        pass

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            self['Cost (£)'] *= other
            self['protein (g/amount)'] *= other
            self['calories (g/amount)'] *= other
        return self

    def __add__(self, other: dict):
        if type(other) == type(self):
            self['Cost (£)'] += other['Cost (£)']
            self['protein (g/amount)'] += other['protein (g/amount)']
            self['calories (g/amount)'] += other['calories (g/amount)']
            return self
        else:
            raise TypeError


class Food(Nutrition):
    '''
    Assumptions:
    Units of amount assumes 1L = 1Kg of substance
    Every protein/calorie is standardized per units of amount
    Each food is assumed to have values corresponding ot (100g)

    Params:
    ---
    name : str, name of the food
    cost : float, cost of the food for 100g
    protein: float, amount of proteins in food for 100g
    calories: int, number of calories in 100g of the food
    '''

    def __init__(self, name, cost, protein, calories):
        self['Name'] = name
        self['Cost (£)'] = cost
        self['protein (g/amount)'] = protein
        self['calories (g/amount)'] = calories


class Meal(Nutrition):
    '''
    A Meal is a collection of foods
    Params:
    ---
    recipe : list, a list of foods
    '''

    def __init__(self, recipe: 'list[Food]', name: str):
        self.recipe = recipe
        self.name = name

    @property
    def get_total(self):
        first_food = self.recipe[0]
        for food in self.recipe[1:]:
            first_food += food
        first_food["Name"] = self.name
        return first_food


class Diet(Nutrition):

    def __init__(self, meals: str,  week_day: str):
        self.week_day = week_day
        self.meals = meals

    @property
    def get_total(self):
        first_meal = self.meals[0]
        for meal in self.meals[1:]:
            first_meal += meal
        first_meal["Name"] = self.week_day
        return first_meal


if __name__ == "__main__":
    test_food1 = Food("food1", 0.1, 0.2, 20)
    test_food2 = Food("food2", 0.2, 0.3, 22)
    test_meal1 = Meal([test_food1, test_food2], "meal1")
    test_meal2 = Meal([test_food1], "meal2")
    test_diet = Diet([test_meal1.get_total, test_meal2.get_total], "diet1")
    print("food", test_food1)
    print("meal", test_meal1.get_total)
    print("diet", test_diet.get_total)
