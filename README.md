# Protocol Backend

In order to build the protocol backend you can use the following diagramming tool,
with the latest version being the [following](https://drawsql.app/teams/university-of-sheffield/diagrams/my-routine)
At the latest the database schema looks like the following

<div style="width:100%; display:flex; justify-content:center; align-items;center;">
<img src="./SCHEMA.png" style="width:98%;">
</div>

The code that is exported can then be modified in virtual studio code as follows:

- include all the primary key statement of id at the bottom of the table
- remove all the backticks
- remove all the unsigned stuff
- make the ids not null for the sql server and then remove the not null for the python script

The current script looks like the following:

```sql
CREATE TABLE Session(
    id INT NOT NULL AUTO_INCREMENT,
    session_id DATETIME NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE Food(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    calories INT NOT NULL,
    protein INT NOT NULL,
    cost INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Meal(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    meals INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Diet(
    id INT NOT NULL AUTO_INCREMENT,
    week_day VARCHAR(255) NOT NULL,
    session_id DATETIME NOT NULL,
    meals INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Exercise(
    id INT NOT NULL AUTO_INCREMENT,
    reps INT NOT NULL,
    sets INT NOT NULL,
    weight INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Workout(
    id INT NOT NULL AUTO_INCREMENT,
    exercises INT NOT NULL,
    session_id DATETIME NOT NULL,
    week_day VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Fitness(
    id INT NOT NULL AUTO_INCREMENT,
    session_id DATETIME NOT NULL,
    maintanace_calories INT NOT NULL,
    muscle_mass INT NOT NULL,
    body_fat INT NOT NULL,
    weight INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE Expenses(
    id INT NOT NULL AUTO_INCREMENT,
    category VARCHAR(255) NOT NULL,
    amount INT NOT NULL,
    session_id DATETIME NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE
    Diet ADD CONSTRAINT diet_meals_foreign FOREIGN KEY(meals) REFERENCES Meal(id);
ALTER TABLE
    Workout ADD CONSTRAINT workout_exercises_foreign FOREIGN KEY(exercises) REFERENCES Exercise(id);
ALTER TABLE
    Meal ADD CONSTRAINT meal_meals_foreign FOREIGN KEY(meals) REFERENCES Food(id);
```

To test the created database you can insert some test data as follows

```sql
INSERT INTO Session (session_id) VALUES ('2022-04-22 10:34:53.44');
INSERT INTO Expenses (category, amount, session_id) VALUES
("transport",5, '2022-04-22 10:34:53.44');
```

finally you can get one of the columns of one of the tables to see what it looks like

```sql
SELECT * FROM Expenses;
```

and this is what the data looks like

<div style="width:100%; display:flex; justify-content:center; align-items;center;">
<img src="./Test_example.png" style="width:40%;">
</div>

The final python code to run on sqlite is:

```python
SQL_STATEMENTS = ['''
CREATE TABLE Session(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id DATETIME NOT NULL
);''', '''
CREATE TABLE Food(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    calories FLOAT NOT NULL,
    protein FLOAT NOT NULL,
    cost FLOAT NOT NULL
);''', '''

CREATE TABLE Meal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    recipe INT NOT NULL,
    FOREIGN KEY(recipe) REFERENCES Food(id)
);''', '''

CREATE TABLE Diet(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_day VARCHAR(255) NOT NULL,
    session_id DATETIME NOT NULL,
    meals INT NOT NULL,
    FOREIGN KEY(meals) REFERENCES Meal(id)
);''', '''

CREATE TABLE Exercise(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reps INT NOT NULL,
    sets INT NOT NULL,
    weight FLOAT NOT NULL,
    name VARCHAR(255) NOT NULL
);''', '''

CREATE TABLE Workout(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercises INT NOT NULL,
    session_id DATETIME NOT NULL,
    week_day VARCHAR(255) NOT NULL,
    FOREIGN KEY(exercises) REFERENCES Exercise(id)
);''', '''

CREATE TABLE Fitness(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id DATETIME NOT NULL,
    maintanace_calories FLOAT NOT NULL,
    muscle_mass FLOAT NOT NULL,
    body_fat FLOAT NOT NULL,
    weight FLOAT NOT NULL
);''', '''

CREATE TABLE Expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    session_id DATETIME NOT NULL
);''']
```

to convert the statements into sqlite3 friendly statements you can run

- replace the `id INT NOT NULL AUTO_INCREMENT` in sql with the `id INTEGER PRIMARY KEY AUTOINCREMENT`
- remove the alter statements at the bottom `ALTER TABLE Meal ADD CONSTRAINT meal_meals_foreign FOREIGN KEY(meals) REFERENCES Food(id);` with constraints to add this ` FOREIGN KEY(exercises) REFERENCES Exercise(id)`
to the correct table
- use ``cntrl + F2`` on ``);`` to add `` ''',''' `` and wrap the entire code with ``[''' ''']``
