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

