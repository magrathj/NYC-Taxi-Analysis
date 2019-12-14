# Big Data - NYC Taxi Data Analysis & Time Series Forecasting

This repo provides scripts to download, process, and analyze data for billions of taxi and for-hire vehicle (Uber, Lyft, etc.) trips originating in New York City since 2009. The data is stored in a PostgreSQL database, and uses PostGIS for spatial calculations.

Statistics through June 30, 2019:

* 2.45 billion total trips
* 1.65 billion taxi
* 800 million for-hire vehicle
* 279 GB of raw data
* Database takes up 378 GB on disk with minimal indexes


### Instructions to use in Azure Postgres instance of Postgres and PostGIS

1. Create an instance of Postgres in Azure

2. Download raw data
`python Setup/download_data.py`

3. Modify paths in the config.py script and run it to load the csv data into the DB. Then populate the database:
`python Setup/etl_db.py --host="<server-name>" --port=5432 --user="<admin-username>" --dbname="<database-name>" --password="<admin-password>" --sslmode="require"` 

4. Analysis
Additional Postgres and R scripts for analysis are in the analysis/ folder


### Instructions to use in local instance of Postgres and PostGIS

1. Install Docker

2. To run the server:
`docker run -d --name ht_pg_server -v ht_dbdata:/var/lib/postgresql/data -p 54320:5432 postgres:11`

3. Check the logs to see if it is running:
`docker logs -f ht_pg_server`

4. Create the database:
`docker exec -it ht_pg_server psql -U postgres -c "create database postgres"`

5. Download raw data
`python Setup/download_data.py`

6. Modify paths in the config.py script and run it to load the csv data into the DB. Then populate the database:
`python Setup/etl_db.py --host="localhost" --port=5432 --user="<admin-username>" --dbname="postgres" --password="<admin-password>" --sslmode="allow"`

7. Analysis
Additional Postgres and R scripts for analysis are in the analysis/ folder, or you can do your own!


### useful links
* https://toddwschneider.com/posts/analyzing-1-1-billion-nyc-taxi-and-uber-trips-with-a-vengeance/
* http://strimas.com/spatial/hexagonal-grids/
* https://github.com/toddwschneider/nyc-taxi-data
* https://chih-ling-hsu.github.io/2018/05/14/NYC#location-data
* https://docs.microsoft.com/en-us/azure/postgresql/quickstart-create-server-database-portal
* https://docs.microsoft.com/en-us/azure/postgresql/connect-python
* https://towardsdatascience.com/if-taxi-trips-were-fireflies-1-3-billion-nyc-taxi-trips-plotted-b34e89f96cfa
