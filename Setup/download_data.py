import sys
import os
from config import *
import pandas as pd
import numpy as np
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError
import zipfile


def download_file(url, path):
    try:
        response = urllib.request.urlretrieve(url, path)
    except URLError as e:
        print("********* ERROR *************")
        print("url: ", url, " has exception ")
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
 

def download_all_urls():
    print("\n Starting Download of CSVs \n")
    with open(urls_path) as fp:
        for cnt, line in enumerate(fp):
            print("Line {}: {}".format(cnt, line))
            file_name = line.split('/')[-1].split('.')[0]
            file_type = file_name.split('_')[0]
            download_file(line, downloads_path.joinpath(f"{file_name}.csv"))
    print("\n Completed Downloading CSVs \n")
       

def download_taxi_zones_shape_file(): 
    print("\n Starting Download of Shape File \n")
    download_file("https://s3.amazonaws.com/nyc-tlc/misc/taxi_zones.zip", downloads_path.joinpath(f"taxi_zones.zip")) 
    directory = downloads_path.joinpath(f"taxi_zones_shape")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with zipfile.ZipFile(downloads_path.joinpath(f"taxi_zones.zip"),"r") as zip_ref:
        zip_ref.extractall(directory)
    print("\n Completed Download of Shape File \n")


def download_NYC_Census_Track_Shape_file():
    print("\n Starting Download of Shape File \n")
    download_file("https://data.cityofnewyork.us/api/geospatial/fxpq-c8ku?method=export&format=Shapefile", downloads_path.joinpath(f"nyc_2010.zip")) 
    directory = downloads_path.joinpath(f"nyc_2010_shape")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with zipfile.ZipFile(downloads_path.joinpath(f"nyc_2010.zip"),"r") as zip_ref:
        zip_ref.extractall(directory)
    print("\n Completed Download of Shape File \n")
    

def extras_download():
    print("\n Starting Download of Base Files \n")
    base_files = ['https://data.cityofnewyork.us/api/views/2v9c-2k7f/rows.csv?accessType=DOWNLOAD','https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv']
    download_file(base_files[0], downloads_path.joinpath(f"base_fhv.csv")) 
    download_file(base_files[1], downloads_path.joinpath(f"lookup.csv")) 
    print("\n Completed Download of Base Files \n")


def main():
    print("***** Starting Download Script ******")
    download_all_urls()
    download_taxi_zones_shape_file()
    download_NYC_Census_Track_Shape_file()
    extras_download()
    print("***** Ending Download Script ******")

if __name__ == '__main__':
    main()
