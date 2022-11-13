import time
import os
import unittest
from pathlib import Path
from os import path
try:
    from src.protocol_backend.sql_db_interface.database_client import DatabaseClient
except ModuleNotFoundError as err:
    print(err)
    from protocol_backend.sql_db_interface.database_client import DatabaseClient

TEST_DATABASE_PATH = "test_database.db"
if path.exists(TEST_DATABASE_PATH):
    print("os removed the database")
    os.remove(TEST_DATABASE_PATH)


class TestDatabaseClient(unittest.TestCase):

    def setUp(self) -> None:
        '''Run at the start of each tests
        * create the testing database table
        * get the path of the database
        * get the number of columns before the test runs'''

        # initialise the path of the test database
        self.db_path = Path(TEST_DATABASE_PATH)

    def test_connection(self):
        '''test that the database is created 
        and some values can be inserted and retrieved'''

        # declare all the sql statements
        create_test_table_statement = '''
CREATE TABLE test_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
)    
        '''
        insert_test_value_statement = '''INSERT INTO test_table(name) VALUES ("test_name")'''
        retrieve_test_value_statement = '''SELECT name FROM test_table'''

        sql_statements: list[str] = [create_test_table_statement,
                                     insert_test_value_statement,
                                     insert_test_value_statement, retrieve_test_value_statement]
        with DatabaseClient(self.db_path) as db:
            # iterate over each SQL statement
            for sql_statement in sql_statements:
                print(sql_statement)
                db.cursor.execute(sql_statement)
                # commit each statement after execution
                db.connection.commit()
                for row in db.cursor:
                    print("this is the row", row['name'])

    def tearDown(self):
        '''Runs after each tests
        * delete the testing database table
        '''

        # declare all the sql statements that will be executed
        delete_database_statement = '''DROP TABLE test_table;'''
        with DatabaseClient(self.db_path) as db:
            print(delete_database_statement)
            db.cursor.execute(delete_database_statement)
            db.connection.commit()


if __name__ == "__main__":
    unittest.main()
