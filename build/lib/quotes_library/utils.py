import sqlite3, os, csv, inspect, sys
from sqlite3 import Error
import requests

DB_URL = "https://github.com/mymi14s/quotes_library/raw/refs/heads/production/quotes_library/db.sqlite3?download="

def download_database(path):
    """Download the database file from GitHub if it's missing or small."""
    # Check if the file already exists and is sufficiently large
    if os.path.exists(path) and os.path.getsize(path) >= 100 * 1024 * 1024:
        return True, None

    print(f"Downloading database to {path}... This may take a while (approx 114MB).")
    try:
        response = requests.get(DB_URL, stream=True)
        response.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
        return True, None
    except Exception as e:
        return False, f"Failed to download database: {str(e)}"

def is_valid_sqlite_file(path):
    """Check if the file is a valid SQLite database."""
    # First, attempt to ensure the file exists and is of correct size via the download manager
    success, error = download_database(path)
    if not success:
        return False, error
    
    # Check for Git LFS pointer explicitly or invalid header
    try:
        with open(path, 'rb') as f:
            header = f.read(100)
            if b'version https://git-lfs.github.com/spec/v1' in header:
                # If it's an LFS pointer, it means the size check passed but it's still a pointer (unlikely)
                # Force a re-download or just report error
                success, error = download_database(path)
                if not success:
                    return False, error
            
            f.seek(0)
            header_sqlite = f.read(16)
            if header_sqlite != b'SQLite format 3\x00':
                return False, "The file is not a valid SQLite database."
    except Exception as e:
        return False, f"Error checking database file: {str(e)}"
    
    return True, None

_db_path = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(is_valid_sqlite_file))), 'db.sqlite3')

def get_db_path():
    return _db_path

def set_db_path(path):
    global _db_path
    _db_path = path

def convert_quotes_to_json(csvfile):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS Quote (id INTEGER PRIMARY KEY, author TEXT, category Text, quote Text)''')
    with open(csvfile, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if len(row) >= 3:
                    conn.execute(
                        "INSERT INTO Quote (quote, author, category) VALUES (?, ?, ?)",
                        (row[0], row[1], row[2])
                    )
                line_count += 1
                
    conn.commit()
    conn.close()

def query_db(query_text, params=None):
    if params is None:
        params = []
    
    db_path = get_db_path()
    valid, error_msg = is_valid_sqlite_file(db_path)
    if not valid:
        return {'data': [], 'status_code': 500, 'status_text': error_msg}

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        records = cursor.execute(query_text, params).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in records]
        return {'data': unpacked, 'status_code': 200, 'status_text':'success'}
    except Error as e:
        return {'data': [], 'status_code': 500, 'status_text':str(e)}
    finally:
        if conn:
            conn.close()


