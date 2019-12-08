import psycopg2 as pg
import yaml
from pathlib import Path
import os
import pandas as pd
import configparser
from config import *


def load_config() -> list:
    with open(schema_path) as schema_file:
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

def load_tables(
    config: list, connection: pg.extensions.connection, prefix: str=None
):
    # Iterate and load
    cur = connection.cursor()
    for table in config:
        table_name = table.get('name')
        table_name_csv = table_name if not prefix else prefix + table_name
        table_source = data_path.joinpath(f"{table_name_csv}.csv")
        print("""Started to load {} data to db from {}.""".format(table_name, table_source))
        with open(table_source, 'r', encoding='utf-8') as f:
            next(f)
            cur.copy_expert(f"COPY {table_name} FROM STDIN CSV NULL AS ''", f)
        connection.commit()
        print("""Completed loading {} table.""".format(table_name))

def etl():
    # DB connection
    print("""ETL started.""")
    print("""Establishing connection to database {} listening on {}, port {} with user name: {}.""".format(dbname, host, port, user))
    connection = pg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user
    )
    print("""Successfully created db connection.""")
    # Table creation and data insertion
    csv_prefix = 'rev-'
    config = load_config()
    create_tables(config=config, connection=connection)
    load_tables(config=config, connection=connection, prefix=csv_prefix)
    print("""ETL completed.""")

if __name__ == '__main__':
    etl()
