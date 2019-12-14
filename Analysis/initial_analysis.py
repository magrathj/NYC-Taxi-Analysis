import pandas as pd
import numpy as np
import os
from pathlib import Path
import sys
sys.path.insert(0, r'.')

from Setup.config import *


downloads = [filename for filename in os.listdir(downloads_path) if filename.startswith("green")]

for file in downloads:
    df = pd.read_csv(downloads_path.joinpath(f"{downloads[0]}"), nrows=10)
    if df.shape[1] != 20:
        print(""" file {} .""".format(file))        
        print(""" count {} .""".format(df.head))

