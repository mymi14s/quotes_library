import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import is_valid_sqlite_file, set_db_path

class TestAutoDownload(unittest.TestCase):
    @patch('utils.requests.get')
    def test_download_trigger_when_file_small(self, mock_get):
        # Create a small "fake" database (LFS pointer style)
        test_db = "fake_lfs.sqlite3"
        with open(test_db, "w") as f:
            f.write("version https://git-lfs.github.com/spec/v1\noid sha256:...\nsize 114270208")
        
        # Mock response for requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"SQLite format 3\x00", b"some data"]
        mock_get.return_value = mock_response
        
        try:
            # This should trigger download_database because file size < 100MB
            valid, error = is_valid_sqlite_file(test_db)
            
            # Verify requests.get was called
            self.assertTrue(mock_get.called)
            # After "download", the file should have SQLite header
            with open(test_db, "rb") as f:
                self.assertEqual(f.read(16), b"SQLite format 3\x00")
        finally:
            if os.path.exists(test_db):
                os.remove(test_db)

if __name__ == '__main__':
    unittest.main()
