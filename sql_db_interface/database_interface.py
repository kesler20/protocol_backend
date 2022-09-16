from sql_db_interface.database_client import DatabaseClient
from sql_db_interface.table_schema import SQL_STATEMENTS

'''The database interface should allow you to implement different database clients from a single Object
The notes for the SQL queries can be found here 
https://github.com/kesler20/Config_settings/blob/master/mySQL/notes.md

The notes for the sqlite3 documentation in python can be found here 
https://docs.python.org/3/library/sqlite3.html#cursor-objects
'''


class DatabaseInterface(object):
    '''The database interface is used to perform CRUD operations on various form of databases i.e. SQL 

    Properties:
    * client - the client is an SQLClient object yielded by the context manager

    The Database Interface supports CRUD operations on tables with the following format:

    ```sql
    test_table_parent
    id integer primary_key autoincrement
    name varchar(255) not null
    ```

    ```sql
    test_table_child
    id integer primary_key autoincrement
    name varchar(255) not null
    foreign key (parent_id) references test_table_parent(id)
    ```

    the type of data to insert is
    | id  | name        | foreign key |
    | --- | ----------- | ----------- |
    | 1   | test_data n | 1           |
    '''

    def __init__(self, client: DatabaseClient) -> None:
        self.client = client

    def run_query(self, query: str, key: str) -> list:
        '''Run a query on the selected database

        params:
        * query - str, the query that will be performed to the database
        * key - str, the key that will be used to retrieve the values within the query
        if the key is left as "" this will be ignored 

        returns:
        * result - list, list of values'''

        result = []
        with self.client as client:
            print(query)
            query_values = client.cursor.execute(query)
            client.connection.commit()

            if key == "":
                pass
            else:
                for value in query_values:
                    result.append(value[key])

        if result == []:
            print(result)

        return result

    def create_tables(self, table_name: str) -> None:
        '''Creates a table

        params:
        * table_name - str, name iof the table to create
        '''
        create_table_sql_statement = '''CREATE TABLE {}(id, year, name)'''.format(
            table_name)
        with self.client as client:
            client.cursor.execute(create_table_sql_statement)
            print(create_table_sql_statement)
            client.connection.commit()

    def update_tables(self, sql_statement: str) -> None:
        '''Update tables 

        params:
        * sql_statement - str, an sql statement that will be run on an existing table
        '''
        with self.client as client:
            client.cursor.execute(sql_statement)
            print(sql_statement)
            client.connection.commit()

    def delete_tables(self, table_name: str) -> None:
        '''Deletes the selected table from the database

        params:
        * table_name - str, name of the table to delete from the database'''

        sql_statement = '''DROP TABLE {}'''.format(table_name)
        with self.client as client:
            client.cursor.execute(sql_statement)
            print(sql_statement)
            client.connection.commit()

    def create_values(self, columns: str, values: list[tuple], table_name: str) -> None:
        '''Create the values

        params:
        * columns - tuple, a tuple containing the columns you want to insert into
        * values - list, a list of tuples of values that you want to insert into the table
        * table_name - str, the name of the table which we want to modify'''

        sql_statement = f'''INSERT INTO {table_name} {columns} VALUES {values}'''
        with self.client as client:
            print(sql_statement)
            client.cursor.execute(sql_statement)
            client.connection.commit()

    def read_all_values(self, column_name: str, table_name: str) -> list:
        '''Read all values within the database

        param:
        * table_name - str, the name of the table we want to read the values of
        * column_name - str, the name of the column we want to read the values of

        returns:
        * values - list, a list of tuples of values'''

        result = []
        sql_statement = f'''SELECT {column_name} FROM {table_name}'''
        with self.client as client:
            values = client.cursor.execute(sql_statement)
            print(sql_statement)
            client.connection.commit()
            for value in values:
                result.append(value[column_name])

        print(result)
        return result

    def read_value(self, column_name: str, table_name: str, primary_key: int, parent_id: str) -> list:
        '''Read all values within the database

        param:
        * table_name - str, the name of the table we want to read the values of
        * column_name - str, the name of the column we want to read the values of
        * primary_key - int, the primary key of the value that we want to retrieve
        * parent_id - the name of the foreign key which references to the parent table

        returns:
        * values - list, a list of tuples of values'''

        result = []
        sql_statement = f'''SELECT {column_name} FROM {table_name} WHERE {parent_id} = {primary_key}'''
        with self.client as client:
            values = client.cursor.execute(sql_statement)
            print(sql_statement)
            client.connection.commit()
            for value in values:
                result.append(value[column_name])
        print(result)
        return result

    def update_value(self, column_name: str, table_name: str, primary_key: int, value: str, parent_id: str) -> None:
        '''Update a value within the database

        param:
        * table_name - str, the name of the table we want to read the values of
        * column_name - str, the name of the column we want to read the values of
        * primary_key - int, the primary key of the value that we want to retrieve
        * parent_id - the name of the foreign key which references to the parent table
        '''

        sql_statement = f'''UPDATE {table_name} SET {column_name} = "{value}" WHERE {parent_id} = {primary_key}'''
        with self.client as client:
            print(sql_statement)
            client.cursor.execute(sql_statement)
            client.connection.commit()

    def delete_value(self, table_name: str, primary_key: int,parent_id: str) -> None:
        '''Delete a value from the table

        param:
        * table_name - str, the name of the table we want to read the values of
        * primary_key - int, the primary key of the value that we want to retrieve
        * parent_id - the name of the foreign key which references to the parent table
        '''

        sql_statement = f'''DELETE FROM {table_name} WHERE {parent_id} = {primary_key}'''
        with self.client as client:
            print(sql_statement)
            client.cursor.execute(sql_statement)
            client.connection.commit()

    def delete_all_values(self, table_name: str) -> None:
        '''Delete all values within the database

        param:
        * table_name - str, the name of the table we want to read the values of
        '''

        delete_statement = f'''DELETE FROM {table_name}'''
        with self.client as client:
            print(delete_statement)
            client.cursor.execute(delete_statement)
            client.connection.commit()


if __name__ == "__main__":
    client = DatabaseClient("my_routine.db")
    db = DatabaseInterface(client)
    for statement in SQL_STATEMENTS:
        print(statement)
        db.run_query(statement, "")

# TODO: enrich the design with proper ways to check if the database table exists etc
# TODO: you can use the row factory to access all the values returned by the cursors
# TODO: functions need to be generalized to any database schema