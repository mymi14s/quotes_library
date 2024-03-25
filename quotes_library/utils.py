import sqlite3, os, csv, inspect
from sqlite3 import Error

def convert_quotes_to_json(csvfile):
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS Quote (id INTEGER PRIMARY KEY, author TEXT, category Text, quote Text)''')
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(line_count, '\n')
                if len(row[0].split(' '))>1:
                    row[0] = row[0].replace('"', "'")
                    row[1] = row[1].replace('"', "'")
                    row[2] = row[2].replace('"', "'")
                    conn.execute(f"""
                        INSERT INTO Quote (quote, author, category)
                        VALUES ("{row[0]}", "{row[1]}", "{row[2]}")
                    """)
                line_count += 1
                
        print(f'Processed {line_count} lines.')
    conn.commit()
    conn.close()

db_path =os.path.abspath(inspect.getfile(convert_quotes_to_json)).replace('utils.py','db.sqlite3')

def query_db(query_text):

    conn = None
    try:
        # Attempt to connect to the SQLite database
        conn = sqlite3.connect(db_path)
        # This makes the row results accessible by column name
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        # Execute the query and fetch all results
        records = cursor.execute(query_text).fetchall()
        # Unpack the records into a list of dictionaries
        unpacked = [{k: item[k] for k in item.keys()} for item in records]
        conn.close()
        return {'data': unpacked, 'status_code': 200, 'status_text':'success'}
    except Error as e:
        return {'data': [], 'status_code': 500, 'status_text':str(e)}
    finally:
        if conn:
            conn.close()


