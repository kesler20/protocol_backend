from datetime import datetime
import pandas as pd
from sql_db_interface.database_interface import DatabaseInterface
from sql_db_interface.database_client import DatabaseClient

'''Week days should allow you to plan the activity in advance for the rest of the week'''

SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M.%S'
client = DatabaseClient(r"sql_db_interface\my_routine.db")
db = DatabaseInterface(client)
SESSION_ID = datetime.now().strftime(SQL_DATETIME_FORMAT)


if __name__ == "__main__":
    # Get Exercise data
    exercises = pd.read_csv(r"C:\Users\Uchek\OneDrive\Documents\exercises.csv")
    exercises_names = list(exercises.keys())[1:]
    # [[weight] # [sets] # [reps]]
    exercises_values = [tuple(exercises[col]) for col in exercises_names]

    # Get Workout data
    workout = pd.read_csv(r"C:\Users\Uchek\OneDrive\Documents\training.csv")
    workout_exercises = list(workout.keys())[1:]
    # [ exercise_id : int, ....]
    workout_values = list(
        map(lambda exercise: exercises_names.index(exercise), workout_exercises))

    # Fitness column data
    fitness = pd.read_excel(
        r"C:\Users\Uchek\OneDrive\Documents\Gymnasium.xlsx")
    fitness_columns = list(fitness.keys())[1:]
    fitness_session_ids = [date.to_pydatetime().strftime(
        SQL_DATETIME_FORMAT) for date in fitness["Date"]]
    # [weight] # [body_fat] # [calories]
    fitness_values = [list(fitness[col]) for col in fitness_columns]
    # [(weight,body_fat,calories)]
    zipped_columns = []
    for row in fitness[fitness_columns[0]]:
        zipped_columns.append(list(zip(*[fitness_values[colID]
                                            for colID, col in enumerate(fitness_columns)])))

    db.create_values("(session_id)", f'''("{SESSION_ID}")''', "Session")

    # Insert Exercise
    print("---------------Insert Exercise----------------")
    for valID, value in enumerate(exercises_values):
        values = tuple([exercises_names[valID], *value])
        db.create_values("(name,weight,sets,reps)", f'{values}', "Exercise")

    # Insert Workout
    print("---------------Insert Workout----------------")
    for workout_id in workout_values:
        db.create_values("(exercises,week_day,session_id)",
                            f"({workout_id},'Monday','{SESSION_ID}')", "Workout")

    # Insert Fitness
    print("---------------Insert Fitness----------------")
    for row in zipped_columns:
        for rowID, rowValues in enumerate(row):
            values = tuple(
                [rowValues[0]*(1-rowValues[1]/100), *rowValues, f'{fitness_session_ids[rowID]}'])
            db.create_values(
                "(muscle_mass, weight,body_fat,maintanace_calories,session_id)", f"{values}", "Fitness")


# TODO: improve how the weak days and session ids are stored so that they correspond to what it is written to excel
 