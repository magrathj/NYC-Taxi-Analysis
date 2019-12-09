import os
from pathlib import Path

os.environ['HOME'] = "C:/Users/jmagr"
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


#Set db variables
os.environ['HOST'] = ""
port=5432
os.environ['DB'] = ""
os.environ['USER'] = ""
os.environ['PASSWORD'] = ""

