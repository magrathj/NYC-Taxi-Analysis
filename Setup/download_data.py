import sys
import os
from config import *
import pandas as pd
import numpy as np
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError
import zipfile
import progressbar


class MyProgressBar():
    ''' 
    Class MyProgressBar
    Description: Monitor progress of each individual download using progress bar
    url: https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve
    '''
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()

def intersection(lst1, tuple1): 
    lst2 = []
    for x in tuple1:
        for y in lst1:
            if x[1]==y:
                lst2.append(x[0])
    return lst2

def merge_lists_to_tuple(list1, list2):       
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list

def check_downloaded_files():
    ''' 
    check_downloaded_files func

    Description:
    function to check whether the files in the url list have already been 
    downloaded to the download directory.

    If none have been downloaded yet, it will just return the url_list
    in the urls_path. Whereas, if some files have been then it will
    return only file still left to be downloaded.
    
    returns: returns a list of urls to still download
    '''
    # get url & download lists
    url_list = [line.rstrip('\n') for line in open(urls_path)]
    downloads = [filename for filename in os.listdir(downloads_path)]
    # url_list to be the same as file names in download directory
    file_names = [x.split('/')[-1] for x in url_list]
    # create a tuple and then find which files have already been downloaded
    merged_file_names = merge_lists_to_tuple(url_list, file_names)
    matches = intersection(downloads, merged_file_names)
    # get a final list of urls still to download
    url_updated_list = [item for item in url_list if item not in matches]
    return url_updated_list


def download_file(url, path):
    try:
        response = urllib.request.urlretrieve(url, path, MyProgressBar())
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
    # check url list against those already downloaded
    url_list = check_downloaded_files()
    for cnt, line in enumerate(url_list):
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
    urllib.request.urlretrieve(base_files[0], downloads_path.joinpath(f"base_fhv.csv")) 
    urllib.request.urlretrieve(base_files[1], downloads_path.joinpath(f"lookup.csv")) 
    print("\n Completed Download of Base Files \n")


def main():
    print("***** Starting Download Script ******")
    # get all csv files for fhv, green & yellow taxis
    download_all_urls()
    # get the shape files for NYC
    download_taxi_zones_shape_file()
    # get the census shape file
    download_NYC_Census_Track_Shape_file()    
    # get meta data
    extras_download()
    print("***** Ending Download Script ******")

if __name__ == '__main__':
    main()
