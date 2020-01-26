from Setup.download_data import * 

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
    # for example - python get_data.py 
    main()