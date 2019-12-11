import os
from pathlib import Path

os.environ['HOME'] = "C:/Users/jmagr"
os.environ['PROJECT'] = "Documents/NYC-Taxi-Analysis"

#Set path
downloads_path = Path(
        os.environ['HOME'],
        'Downloads/NYC_Data_Test'
    )

schema_path = Path(
        os.environ['HOME'],
        os.environ['PROJECT'],
        'Setup',
        'schemas.yaml'
    )

urls_path = Path(
        os.environ['HOME'],
        os.environ['PROJECT'],
        'Setup',
        'urls.txt'
    )

data_path =  Path(
        os.environ['HOME'],
        os.environ['PROJECT'],
        'data'
    )


