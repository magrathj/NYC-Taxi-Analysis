import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession
import zipfile, io, os
import pandas as pd 
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import col, when
from functools import reduce
from pyspark.sql import SQLContext
import glob
from config import *
import yaml

spark = SparkSession.builder.appName("ETL Process").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.enabled", "true")


def get_downloaded_files(file_prefix):
    files = [filename for filename in os.listdir(downloads_path) if filename.startswith(file_prefix)]
    return files

def get_spark_df(filename, type='csv', header='true', mode='DROPMALFORMED', inferSchema='true'):
    df = spark.read.format(type)\
            .option("header", header)\
            .option("mode", mode)\
            .option("inferSchema", inferSchema)\
            .load(filename) 
    return df

def rename_columns(df, columns):
    if isinstance(columns, dict):
        for old_name, new_name in columns.items():
            df = df.withColumnRenamed(old_name, new_name)
        return df
    else:
        raise ValueError("'columns' should be a dict, like {'old_name_1':'new_name_1', 'old_name_2':'new_name_2'}")


def blank_as_null(x):
    return when(col(x) != "", col(x)).otherwise(None)

def convert_blank_as_null(df):
    columnList = [item[0] for item in df.dtypes if item[1].startswith('string')]
    to_convert = set(columnList)
    df = reduce(lambda df, x: df.withColumn(x, blank_as_null(x)), to_convert, df)
    return df

def add_additional_columns(df, col):
    if isinstance(col, dict):
        for col_name, col_datatype in col.items():
            if not col_name in df.columns:
                df = df.withColumn(col_name, lit(None).cast(col_datatype))
        return df
    else:
        raise ValueError("'columns' should be a dict, like {'old_name_1':'new_name_1', 'old_name_2':'new_name_2'}")


def cleanse_files(file_prefix, rename_col, col):
    files = get_downloaded_files(file_prefix=file_prefix)
    for file in files:
        filename = downloads_path.joinpath(file)
        output_file = data_path.joinpath(file)
        df = get_spark_df(filename=filename.as_posix())
        #df = add_additional_columns(df=df, col=col)
        df = rename_columns(df=df, columns=rename_col)
        df = convert_blank_as_null(df=df)
        print(df.printSchema())
        #df.toPandas().to_csv(output_file.as_posix())


def load_config(path) -> list:
    with open(path) as schema_file:
        config = yaml.load(schema_file)
    return config

def etl():
    print("""ETL started.""")
    config = load_config(path=etl_schema_path)
    for file in config:
        file_pre_fix = file.get('name')
        columns_rename = file.get('rename')
        additional_columns = file.get('columns')
        cleanse_files(file_prefix=file_pre_fix, rename_col=columns_rename, col=additional_columns)




