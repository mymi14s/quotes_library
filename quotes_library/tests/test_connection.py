import os
import unittest
import sqlite3
import sys

# Add the parent directory to sys.path to allow importing from quotes_library
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import query_db, set_db_path, get_db_path

class TestQueryDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup: Create a temporary database
        cls.test_db_path = os.path.abspath('test_db.sqlite3')
        cls.original_db_path = get_db_path()
        set_db_path(cls.test_db_path)
        
        conn = sqlite3.connect(cls.test_db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Quote (id INTEGER PRIMARY KEY, author TEXT, category TEXT, quote TEXT)''')
        cursor.execute('''INSERT INTO Quote (author, category, quote) VALUES ('Author1', 'Cat1', 'Quote1')''')
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        # Teardown: Restore original db path and remove the temporary database
        set_db_path(cls.original_db_path)
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_database_connection(self):
        """Test if the database file exists and can be connected to."""
        self.assertTrue(os.path.exists(self.test_db_path), "Database file does not exist.")
        # Perform a query to ensure connection and execution works
        result = query_db("SELECT * FROM Quote")
        self.assertEqual(result['status_code'], 200, f"Database connection or query execution failed: {result.get('status_text')}")
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['author'], 'Author1')

    def test_exception_handling(self):
        """Test if an error occurs in the exception block."""
        # Point to a non-existent/invalid file that doesn't pass is_valid_sqlite_file
        old_path = get_db_path()
        set_db_path('non_existent.sqlite3')
        try:
            result = query_db("SELECT * FROM Quote")
            # Our is_valid_sqlite_file should return 500 for non-existent file
            self.assertEqual(result['status_code'], 500, "Exception handling failed to report error for missing file.")
        finally:
            set_db_path(old_path)

if __name__ == '__main__':
    unittest.main()
