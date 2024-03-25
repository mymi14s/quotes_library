import os
import unittest
import sqlite3
from utils import query_db  # Ensure this imports your query_db function correctly
db_path = 'test_db.sqlite3'

class TestQueryDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup: Create a temporary database
        cls.db_path = 'test_db.sqlite3'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Test (id INTEGER PRIMARY KEY, data TEXT)''')
        cursor.execute('''INSERT INTO Test (data) VALUES ('Hello, world!')''')
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        # Teardown: Remove the temporary database
        os.remove(db_path)

    def test_database_connection(self):
        """Test if the database file exists and can be connected to."""
        self.assertTrue(os.path.exists(db_path), "Database file does not exist.")
        # Perform a query to ensure connection and execution works
        result = query_db("SELECT * FROM Test")
        self.assertEqual(result['status_code'], 200, "Database connection or query execution failed.")

    def test_exception_handling(self):
        """Test if an error occurs in the exception block."""
        # Temporarily rename the database file to simulate a connection error
        os.rename(db_path, 'temp_db.sqlite3')
        try:
            result = query_db("SELECT * FROM Test")
            # Check if the error status code is returned
            self.assertEqual(result['status_code'], 500, "Exception handling failed to report error correctly.")
        finally:
            # Restore the original database file name
            os.rename('temp_db.sqlite3', db_path)

if __name__ == '__main__':
    unittest.main()
