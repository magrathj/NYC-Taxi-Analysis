import pandas as pd
import numpy as np
import os
from pathlib import Path
import sys
sys.path.insert(0, r'.')

from config import *

start_with = "yellow"
path = data_path2
downloads = [filename for filename in os.listdir(path) if filename.startswith(start_with)]

for file in downloads:
    df = pd.read_csv(path.joinpath(f"{file}"), nrows=100)
    #print(f"columns: {df.columns}")
    #print(f"head: {df.head}")

    #for col in df.columns:
    #    print(f"{col}: ")

    for col, type in zip(df.columns, df.dtypes):
        print(f"{col}: {type}")
    


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






