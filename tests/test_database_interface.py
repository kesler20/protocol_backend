import sqlite3
from sql_db_interface.database_client import DatabaseClient
import unittest
from sql_db_interface.database_interface import DatabaseInterface
from tests.test_database_client import TEST_DATABASE_PATH

print("Testing:" + DatabaseInterface.__doc__)

#######################################
#                                    #
#        DATASET FOR TEST CASES      #
#                                    #
######################################

# correct data
data_1 = [
    ("test data 1", 1),
    ("test data 2", 2),
    ("test data 3", 3),
]

data = [
    ["test data 1", 1],
    ["test data 2", 2],
    ["test data 3", 3],
]
# dataset with a null value
data_2 = [
    (None, 7.9),
    ("test data 2", 4),
    ("test data 3", 8.9),
]
# dataset with the wrong number of columns
data_3 = [
    ("test data 1", ),
    ("test data 2", 7.9),
    ("test data 3", 8.9),
]
# empty dataset
data_4 = []


class Test_DatabaseInterface(unittest.TestCase):
    '''Object Description'''

    def setUp(self) -> None:
        '''Set up the database interface'''

        print("\n----------------------SET UP TABLES---------------------------\n")

        # the client is used in the interface to execute all the statements
        self.client = DatabaseClient(TEST_DATABASE_PATH)

        # an instance of the interface is insitalised to call its functions within the test
        self.database_interface = DatabaseInterface(self.client)

        # initialise the sql statements
        create_table_parent_statement = '''CREATE TABLE IF NOT EXISTS test_table_parent(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
        )'''

        create_child_table_statement = '''CREATE TABLE IF NOT EXISTS test_table_child(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            parent_id INTEGER NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES test_table_parent(id)   
        )'''

        insert_some_values_to_the_database_to_delete = '''INSERT INTO test_table_child (name, parent_id) VALUES (? , ?)'''

        sql_statements = [create_table_parent_statement,
                          create_child_table_statement, insert_some_values_to_the_database_to_delete]

        # execute the statements
        with self.client as client:
            for sql_statement in sql_statements:
                if "INSERT" in sql_statement:
                    client.cursor.executemany(sql_statement, data_1)
                else:
                    client.cursor.execute(sql_statement)
                client.connection.commit()

    def test_delete_all_values(self) -> None:
        '''delete all the values within the database table'''

        # implement the function being tested
        self.database_interface.delete_all_values("test_table_child")

        # check the number of columns
        get_number_of_rows_statement = '''SELECT COUNT(id) FROM test_table_child'''
        with self.client as client:
            print(get_number_of_rows_statement)
            number_of_rows = client.cursor.execute(
                get_number_of_rows_statement)
            for row in number_of_rows:
                self.assertEqual(row['COUNT(id)'], 0)
            client.connection.commit()

    def test_auto_increment_id(self) -> None:
        '''increment the primary key id of the table of the database'''

        # get the current number of rows of your database
        get_number_of_rows_statement = '''SELECT id FROM test_table_child'''
        with self.client as client:
            print(get_number_of_rows_statement)
            number_of_rows = client.cursor.execute(
                get_number_of_rows_statement)
            for row in number_of_rows:
                initial_row_id = row['id']
            client.connection.commit()

        # insert two values into the database
        insert_three_values = '''INSERT INTO test_table_child(name, parent_id) VALUES (?,?)'''
        with self.client as client:
            client.cursor.executemany(insert_three_values, data_1)
            client.connection.commit()

        # check that the id column has increased correctly
        get_number_of_rows_statement = '''SELECT id FROM test_table_child'''
        with self.client as client:
            print(get_number_of_rows_statement)
            number_of_rows = client.cursor.execute(
                get_number_of_rows_statement)
            for row in number_of_rows:
                final_row_id = row['id']
            client.connection.commit()

        print("initial row id:", initial_row_id)
        print("final row id:", final_row_id)
        self.assertEqual(initial_row_id + 3, final_row_id)

    def test_create_tables(self) -> None:
        '''Test the creation of a new table'''

        # create a table called new_test_table
        self.database_interface.create_tables("new_test_table")

        # check if the new table exists by selecting its values
        select_new_table_values = '''SELECT * FROM new_test_table'''
        with self.client as client:
            values = client.cursor.execute(select_new_table_values)
            self.client.connection.commit()
            values = values.fetchall()
            print(select_new_table_values)

        # check that the value is an empty array
        self.assertListEqual(values, [])

    def test_update_tables(self) -> None:
        '''Test update table'''

        table_name = '''test_table_child'''
        sql_statement = '''ALTER TABLE {} ADD another_column'''.format(
            table_name)
        self.database_interface.update_tables(sql_statement)

        # run some select query to check if the table exists
        with self.client as client:
            client.cursor.execute(
                '''SELECT another_column FROM {}'''.format(table_name))
            client.connection.commit()

    def test_delete_tables(self) -> None:
        '''Test delete tables'''

        # \ create table to delete
        with self.client as client:
            client.cursor.execute(
                '''CREATE TABLE table_to_delete(column_to_delete)''')
            client.connection.commit()

        self.database_interface.delete_tables("table_to_delete")

        # try to access the table
        with self.client as client:
            try:
                client.cursor.execute(
                    '''SELECT column_to_delete FROM table_to_delete''')
                client.connection.commit()
            except sqlite3.OperationalError as err:
                print(err)

    def test_create_values(self) -> None:
        '''test create values'''

        # insert a value to the database
        self.database_interface.create_values(
            "(name,parent_id)", data_2[1], "test_table_child")

        with self.client as client:
            print(
                f'''SELECT name FROM test_table_child WHERE name = {data_2[1][0]}''')
            names = client.cursor.execute(
                f'''SELECT name FROM test_table_child WHERE name = "{data_2[1][0]}"''')
            client.connection.commit()
            for name in names:
                print("from database:", name["name"])
                print("from dataset:", data_2[1][0])
                self.assertEqual(str(name["name"]), data_2[1][0])

    def test_read_all_values_from_column(self) -> str:
        '''test reading all the values in the table'''
        values = self.database_interface.read_all_values_from_column(
            "name", "test_table_child")
        expected_name_column = [value[0] for value in data_1]
        self.assertEqual(values, expected_name_column)

    def test_read_value(self) -> str:
        '''testing reading a value from the table'''
        value = self.database_interface.read_value(
            "name", "test_table_child", 1)
        self.assertEqual(value[0], data_1[0][0])

    def test_update_value(self) -> None:
        '''testing updating a value from the table'''
        value = "test data n"
        self.database_interface.update_value(
            "name", "test_table_child", 1, value)

        with self.client as client:
            updated_values = client.cursor.execute(
                '''SELECT name FROM test_table_child WHERE parent_id = 1''')
            for updated_value in updated_values:
                updated_value = updated_value["name"]
            client.connection.commit()

        self.assertEqual(value, updated_value)

    def test_delete_value(self) -> None:
        '''testing delete a value from the table'''

        self.database_interface.delete_value("test_table_child", 2)

        with self.client as client:
            values = client.cursor.execute(
                '''SELECT name FROM test_table_child WHERE parent_id = 2''')
            client.connection.commit()
            self.assertEqual(values.fetchall(), [])

    def tearDown(self):
        print("\n---------------------------TEAR DOWN---------------------------\n")

        # implement the function being tested
        self.database_interface.delete_all_values("test_table_child")

        # check the number of columns
        get_number_of_rows_statement = '''SELECT COUNT(id) FROM test_table_child'''
        with self.client as client:
            values = client.cursor.execute(get_number_of_rows_statement)
            for value in values:
                self.assertEqual(value["COUNT(id)"], 0)
            client.connection.commit()


if __name__ == "__main__":
    unittest.main()
