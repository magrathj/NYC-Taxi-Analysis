import psycopg2
import os
import sys
from config import *

def connect():
    # Update connection string information 
    host = sys.argv[1]
    dbname = "postgres"
    user = sys.argv[2]
    password = sys.argv[3]
    sslmode = "require"

    # Construct connection string
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string) 
    print("Connection established")

    cursor = conn.cursor()

    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS inventory;")
    print("Finished dropping table (if existed)")

    # Create a table
    cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    print("Finished creating table")

    # Insert some data into the table
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
    print("Inserted 3 rows of data")

    # Clean up
    conn.commit()
    cursor.close()
    conn.close()

def search_for_downloaded_files():
    prefix = ['fhv', 'green', 'yellow']
    for pre in prefix:
        files = [filename for filename in os.listdir(downloads_path) if filename.startswith(pre)]
        print(files)


def main():
    search_for_downloaded_files()


if __name__ == '__main__':
    main()


    