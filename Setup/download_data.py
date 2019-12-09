import sys
import os
from config import *
import pandas as pd
import numpy as np
import urllib.request
import zipfile


def download_all_urls():
    print("\n Starting Download of CSVs \n")
    with open(urls_path) as fp:
        for cnt, line in enumerate(fp):
            print("Line {}: {}".format(cnt, line))
            file_name = line.split('/')[-1].split('.')[0]
            file_type = file_name.split('_')[0]
            urllib.request.urlretrieve(line, downloads_path.joinpath(f"{file_name}.csv"))
    print("\n Completed Downloading CSVs \n")
       
def download_shape_file(): 
    print("\n Starting Download of Shape File \n")
    urllib.request.urlretrieve("https://s3.amazonaws.com/nyc-tlc/misc/taxi_zones.zip", downloads_path.joinpath(f"taxi_zones.zip")) 
    with zipfile.ZipFile("taxi_zones.zip","r") as zip_ref:
        zip_ref.extractall("./shape")
    print("\n Completed Download of Shape File \n")


def main():
    download_all_urls()
    download_shape_file()


if __name__ == '__main__':
    main()
