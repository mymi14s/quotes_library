import os
import unittest
import sqlite3
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import query_db, set_db_path, get_db_path
from utils import query_db, set_db_path, get_db_path
import main
from main import get_quotes, get_authors, get_categories

class TestLibraryLogic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_path = os.path.abspath('test_logic.sqlite3')
        cls.original_db_path = get_db_path()
        set_db_path(cls.test_db_path)
        
        conn = sqlite3.connect(cls.test_db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Quote (id INTEGER PRIMARY KEY, author TEXT, category TEXT, quote TEXT)''')
        quotes = [
            ('Author A', 'Cat 1', 'Quote 1'),
            ('Author B', 'Cat 1', 'Quote 2'),
            ('Author C', 'Cat 2', 'Quote 3'),
            ('Mark Twain', 'Inspirational', 'Quote from Mark'),
        ]
        cursor.executemany('INSERT INTO Quote (author, category, quote) VALUES (?, ?, ?)', quotes)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        set_db_path(cls.original_db_path)
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_get_quotes_filter_author(self):
        result = get_quotes(author='Author A')
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['author'], 'Author A')

    def test_get_quotes_filter_category(self):
        result = get_quotes(category='Cat 1', count=5)
        self.assertEqual(len(result['data']), 2)

    def test_sql_injection_prevention(self):
        # Malicious author input
        malicious_input = "'; DROP TABLE Quote; --"
        result = get_quotes(author=malicious_input)
        # Should return nothing but NOT fail
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(len(result['data']), 0)
        
        # Verify table still exists
        check = query_db("SELECT name FROM sqlite_master WHERE type='table' AND name='Quote'")
        self.assertEqual(len(check['data']), 1)

    def test_get_authors(self):
        result = get_authors()
        self.assertEqual(result['status_code'], 200)
        self.assertIn('Author A', result['data'])
        self.assertIn('Author B', result['data'])
        self.assertIn('Mark Twain', result['data'])

    def test_get_categories(self):
        result = get_categories()
        self.assertEqual(result['status_code'], 200)
        self.assertIn('Cat 1', result['data'])
        self.assertIn('Cat 2', result['data'])

if __name__ == '__main__':
    unittest.main()
