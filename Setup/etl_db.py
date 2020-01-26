import psycopg2 as pg
import yaml
from pathlib import Path
import os
import pandas as pd
import configparser
from config import *
import sys
import argparse
import re

def check_for_fhv_2017_type(name, files):
    # if months over 7+ cut list
    if name == "fhv_tripdata_2017":
        files = [x for x in files if int(x.split('-')[-1].split('.')[0]) < 7]
    return files

def load_config(path) -> list:
    with open(path) as schema_file:
        config = yaml.load(schema_file)
    return config

def create_tables(config: list, connection: pg.extensions.connection):
    cur = connection.cursor()
    for table in config:
        name = table.get('name')
        schema = table.get('schema')
        ddl = f"""CREATE TABLE IF NOT EXISTS {name} ({schema})"""
        cur.execute(ddl)
        print("""Created {} table.""".format(name))

    connection.commit()
    print("""Commited all creations.""")

def load_tables(config: list, connection: pg.extensions.connection):
    # Iterate and load
    cur = connection.cursor()
    for table in config:
        table_name = table.get('name')
        table_files = [filename for filename in os.listdir(data_path) if filename.startswith(table_name)]
        table_files = check_for_fhv_2017_type(name=table_name, files=table_files)
        if not table_files:
            print("""No files to upload to {} table.""".format(table_name))
        else:
            for file in table_files:
                file_name = file.split('.')[0]
                table_source = data_path.joinpath(f"{file_name}.csv")
                print("""Started to load {} data to db from {}.""".format(table_name, table_source))
                with open(table_source, 'r', encoding='utf-8') as f:
                    next(f)
                    cur.copy_expert(f"COPY {table_name} FROM STDIN CSV NULL AS ''", f)
                connection.commit()
                print("""Completed loading file {} into {} table.""".format(file, table_name))

def load_shape_files(config: list, connection: pg.extensions.connection):
    # Iterate and load
    cur = connection.cursor()
    for table in config:
        table_name = table.get('name')
        table_files = [filename for filename in os.listdir(data_path) if filename.startswith(table_name)]
        table_files = check_for_fhv_2017_type(name=table_name, files=table_files)
        print(table_files)
        if not table_files:
            print("""No files to upload to {} table.""".format(table_name))
        else:
            print("""Files to upload to {} table.""".format(table_name))
            

def etl(host, port, dbname, user, password, sslmode):
    # DB connection
    print("""ETL started.""")
    print("""Establishing connection to database {} listening on {}, port {} with user name: {}.""".format(dbname, host, port, user))
    connection = pg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        sslmode=sslmode
    )
    print("""Successfully created db connection.""")
    # Table creation and data insertion
    config = load_config(path=schema_path)
    create_tables(config=config, connection=connection)
    load_tables(config=config, connection=connection)
    #load_shape_files(config=config, connection=connection)
    print("""ETL completed.""")


def main():
    # Create Argument Parser
    ap = argparse.ArgumentParser(description = "This script creates and loads the NYC Taxi dataset into a defined postgres db. For example, python etl_db.py --host=<server-name> --port=5432 --dbname=<database-name> --user=<admin-username> --password=<admin-password>")
    # Add the arguments to the parser
    ap.add_argument("-s", "--host", required=True, help="Enter <server-name>")
    ap.add_argument("-p", "--port", required=True, help="Enter <port-number>, default 5432")
    ap.add_argument("-d", "--dbname", required=True, help="Enter <database-name>, default postgres")
    ap.add_argument("-u", "--user", required=True, help="Enter <admin-username>")
    ap.add_argument("-a", "--password", required=True, help="Enter <admin-password>")
    ap.add_argument("-m", "--sslmode", required=True, help="ssl required or not - put either require/allow")
    args = vars(ap.parse_args())
    # Set db variables
    host = args['host']
    port = args['port']
    dbname = args['dbname']
    user = args['user']
    password = args['password']
    sslmode = args['sslmode']
    etl(host=host, port=port, dbname=dbname, user=user, password=password, sslmode=sslmode)


if __name__ == '__main__':
    # for example - python Setup/etl_db.py --host="localhost" --port=5432 --user="postgres" --dbname="postgres" --password="password" --sslmode="allow"
    main()
