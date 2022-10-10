BASE_AMOUNT = 100  # g


def calculate_total(recipe) -> dict:
    '''signature description'''
    result = {}
    for food in recipe:
        if recipe.index(food) == 0:
            result["cost"] = 0
            result["protein"] = 0
            result["calories"] = 0
            result["cost"] += food.cost*food.amount/BASE_AMOUNT
            result["protein"] += food.protein*food.amount/BASE_AMOUNT
            result["calories"] += food.calories*food.amount/BASE_AMOUNT
        else:
            result["cost"] += food.cost*food.amount/BASE_AMOUNT
            result["protein"] += food.protein*food.amount/BASE_AMOUNT
            result["calories"] += food.calories*food.amount/BASE_AMOUNT
    return result


class Food(object):
    '''
    Food the unit created by te user which is a dictionary containing the following values
    '''

    def __init__(self, name: str,  cost: float,  protein: float,  calories: int) -> None:
        self.name = name
        self.cost = cost
        self.protein = protein
        self.calories = calories
        self.amount = BASE_AMOUNT


class Meal(object):
    '''
    Meal, a meal is a collection of foods which has also a name, this has a property of total which
    represents a dictionary of the following key value pairs
    '''

    def __init__(self, name: str,  recipe: 'list[Food]') -> None:
        self.name = name
        self.recipe = recipe
        self.total = calculate_total(recipe)


class Diet(object):
    '''
    Diet, a diet is a collection of meals which has a day of the week id, 
    therefore there can only be 7 diets in a week
    '''

    def __init__(self, day: str,  meals: 'list[Meal]') -> None:
        self.day = day
        self.meals = meals
        self.total = calculate_total(meals)


if __name__ == "__main__":
    test_food1 = Food("food1", 0.1, 0.2, 20)
    test_food1.amount = 75
    test_food2 = Food("food2", 0.2, 0.3, 22)
    test_food2.amount = 89
    meal1 = Meal("meal1", [test_food1, test_food2])
    print(meal1.total)
