import os
from pathlib import Path

os.environ['HOME'] = "C:/Users/jmagr/"
os.environ['PROJECT'] = "OneDrive/Documents/Github/NYC-Taxi-Analysis"

#Set path
downloads_path = Path(
        os.environ['HOME'],
        'Downloads/NYC_Data'
    )

schema_path = Path(
        os.environ['HOME'],
        os.environ['PROJECT'],
        'Setup',
        'schemas.yaml'
    )

etl_schema_path = Path(
        os.environ['HOME'],
        os.environ['PROJECT'],
        'ETL',
        'schemas.yaml'
    )

shapefiles_path = Path(
        os.environ['HOME'],
        os.environ['PROJECT'],
        'Setup',
        'shapefiles.yaml'
    )

urls_path = Path(
        os.environ['HOME'],
        os.environ['PROJECT'],
        'Setup',
        'urls.txt'
    )

data_path =  Path(
        os.environ['HOME'],
        'Downloads/NYC_Output_Second'
    )


data_path2 =  Path(
        os.environ['HOME'],
        'Downloads/NYC_Data_Output'
    )

