import pandas as pd
import numpy as np
import os
from pathlib import Path
import sys
sys.path.insert(0, r'.')

from Setup.config import *


downloads = [filename for filename in os.listdir(downloads_path) if filename.startswith("green")]

df = pd.read_csv(downloads_path.joinpath(f"{downloads[0]}"), nrows=10)
template_col = list(df.columns)

for file in downloads:
    df = pd.read_csv(downloads_path.joinpath(f"{file}"), nrows=10)
    if template_col != list(df.columns):
        print(""" file {} .""".format(file))        
        #print(""" count {} .""".format(list(df.columns)))
        #print("------------start--------------")
        #print(""" template {} .""".format(template_col)) 
        #print(""" template2 {} .""".format(template_col_2)) 
        print(""" difference {} """.format( list(set(list(df.columns)) - set(template_col))))
        print(list(df.columns) == template_col)

#df = pd.read_csv(downloads_path.joinpath(f"{downloads[1]}"), nrows=10)
#template_col_2 = list(df.columns)






