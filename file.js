
/*
* Food the unit created by te user which is a dictionary containing the following values
    self['Name'] = name
    self['Cost (£)'] = cost
    self['protein (g/amount)'] = protein
    self['calories (g/amount)'] = calories
- Meal, a meal is a collection of foods whic
*/
export default class Food {
    constructor( name, cost, protein, calories) {
        this.name = name;
        this.cost = cost;
        this.protein = protein;
        this.calories = calories;
    }
}

/*
* Meal, a meal is a collection of foods which has also a name, this has a property of total which
represents a dictionary of the following key value pairs
    self['Cost (£)'] = cost
    self['protein (g/amount)'] = protein
    self['calories (g/amount)'] = calories
*/
export class Meal {
    constructor( name, recipe, total) {
        this.name = name;
        this.recipe = recipe;
        this.total = total;
    }
    
    /*
    * signature description
    */
    calculate_total() {
        return;
    }
}

/*
* - Diet, a diet is a collection of meals which has a day of the week id, therefore there can only be 7 diets in a week
*/
export class Diet {
    constructor( day, meals) {
        this.day = day;
        this.meals = meals;
    }
}
