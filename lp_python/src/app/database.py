"""
file for mysql class and other db functionality
"""
import mysql.connector
from .config import Config


class MySql:
    """
    MySql class that will be used for mysql connections and to retrieve cursor
    Config vars from env file will be used to determine connection params
    messages from this class will start with MYSQL:
    """

    def __init__(self) -> None:
        """
        function that connects to mysql db using env vars and
        sets cursor in class to execute queries
        """
        database = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            passwd=Config.DB_PASSWORD,
        )
        self.connection = database

    def _get_cursor(self):
        return self.connection.cursor(buffered=True, dictionary=True)

    def select_one(self, query_string, query_data=None):
        """
        function to select object from table and return bool if it exists or not
        args:
          query_string - select statement to be executed in proper SQL syntax
          query_data - data to associated with select statement to see if it already exists
        """
        cursor = self._get_cursor()
        try:
            cursor.execute(query_string, query_data)
            result = cursor.fetchone()
            cursor.close()
            if result:
                print("MYSQL: row found for", query_string)
                return result
            else:
                print("MYSQL: no row found for", query_string)
                return None

        except Exception as error:
            print("MYSQL: Error executing query", error)

    def check_if_object_exists(self, query_string, query_data) -> bool:
        """
        function to select object from table and return bool if it exists or not
        args:
          query_string - select statement to be executed in proper SQL syntax
          query_data - data to associated with select statement to see if it already exists
        """
        cursor = self._get_cursor()
        try:
            cursor.execute(query_string, query_data)
            result = cursor.fetchone()
            cursor.close()
            if result:
                print("MYSQL: Object already exists")
                return True
            else:
                print("MYSQL: Object doesn't exist")
                return False

        except Exception as error:
            print("MYSQL: Error executing query", error)

    def insert(self, query_string, query_data) -> str or None:
        """
        function to insert new row into table, it accepts a sql statement string and the data
        associated with the query
        args:
          query_string - insert statment in proper SQL syntax
          (ex: "SELECT * FROM [db_name].[schema_name] WHERE `[col]` = %s")
          query_data - data associated with new row
        """
        cursor = self._get_cursor()
        try:
            cursor.execute(query_string, query_data)
            self.connection.commit()
            cursor.close()
            print("MYSQL: Query Successfully Executed", query_string)
            return cursor.lastrowid
        except Exception as error:
            print("MYSQL: Error executing query", error)


sql_api = MySql()
