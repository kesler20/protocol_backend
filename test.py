from datetime import datetime
import pandas as pd

SESSION_ID = datetime.now()

'''Week days should allow you to plan the activity in advance for the rest of the week'''

# ------------- INITIALISE TABLE DATA -------------- #
# initialise session
session = { "session_id" : SESSION_ID }

# all inters except the reps and sets should be floats
# convert the amount into a float
# from Monzo
expenses = {"category": "transport", "amount": 2, "session_id": SESSION_ID}

# Integrate the amounts later
# change the name from meals to recipes
# change the costs to floats
# from sofia diet
diet = {"week_day": "Monday", "meals": [1, 2], "session_id": SESSION_ID}
meals = {"name": "Protein Shake", "recipe": [1, 2]}
meals = {"name": "Greek Yoghurt & Biscuits", "recipe": [2, 3]}
food = {"name": "Protein Shake", "calories": "800",
        "protein": "70", "cost": "1.3"}

# Even weights need to be floats
workout = {"exercises": [1, 2, 3],
           "week_day": "Monday", "session_id": SESSION_ID}
exercise = {"name": "Bench Press", "reps": 5, "sets": 5, "weight": 105}
# from here
workout = pd.read_csv(r"C:\Users\Uchek\OneDrive\Documents\training.csv")
exercises = pd.read_csv(r"C:\Users\Uchek\OneDrive\Documents\exercises.csv")
print(workout)
print(exercises)


# body_fat can be a float
fitness = {"weight": 86, "body_fat": 19, "muscle_mass": 67,
           "maintanance_calories": 2000, "session_id": SESSION_ID}

# from here
fitness = pd.read_excel(r"C:\Users\Uchek\OneDrive\Documents\Gymnasium.xlsx")
print(fitness)
   