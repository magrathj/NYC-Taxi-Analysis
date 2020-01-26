import pandas as pd
import numpy as np
import os
from pathlib import Path
import sys
sys.path.insert(0, r'.')

from config import *
from pyspark import SparkContext, SparkConf
from pyspark.sql.functions import col, when
from pyspark.sql import SparkSession


spark = SparkSession.builder.appName("Analysis").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.enabled", "true")



start_with = "FHV"
path = data_path2
downloads = [filename for filename in os.listdir(path) if filename.startswith(start_with)]


def df_spark(file, type='csv', header='true', mode='DROPMALFORMED', inferSchema='true'):
    df = spark.read.format(type)\
            .option("header", header)\
            .option("mode", mode)\
            .option("inferSchema", inferSchema)\
            .load(file)\
            .limit(20)
    return df


for file in downloads:
    #df = pd.read_csv(path.joinpath(f"{file}"), nrows=100)
    #print(f"columns: {df.columns}")
    #print(f"head: {df.head}")

    #for col in df.columns:
    #    print(f"{col}: ")

    #for col, type in zip(df.columns, df.dtypes):
    #    print(f"{col}: {type}")
    print(path.joinpath(f"{file}"))
    print(path.joinpath(f"{file}").as_posix())
    path = path.joinpath(f"{file}").as_posix()
    print(f" ---------------------")
    df = df_spark(file=path)
    print(df.printSchema())
    
    


    #if template_col != list(df.columns):
    #    print(""" file {} .""".format(file))        
        #print(""" count {} .""".format(list(df.columns)))
        #print("------------start--------------")
        #print(""" template {} .""".format(template_col)) 
        #print(""" template2 {} .""".format(template_col_2)) 
        #print(""" difference {} """.format( list(set(list(df.columns)) - set(template_col))))
        #print(list(df.columns) == template_col)

#df = pd.read_csv(downloads_path.joinpath(f"{downloads[1]}"), nrows=10)
#template_col_2 = list(df.columns)






