# New York City Taxi and For-Hire Vehicle Data
Code originally in support of this post: "Analyzing 1.1 Billion NYC Taxi and Uber Trips, with a Vengeance"

This repo provides scripts to download, process, and analyze data for billions of taxi and for-hire vehicle (Uber, Lyft, etc.) trips originating in New York City since 2009. Most of the raw data comes from the NYC Taxi & Limousine Commission.

The data is stored in a PostgreSQL database, and uses PostGIS for spatial calculations.

Statistics through June 30, 2019:

* 2.45 billion total trips
* 1.65 billion taxi
* 800 million for-hire vehicle
* 279 GB of raw data
* Database takes up 378 GB on disk with minimal indexes


Instructions
1. Install PostgreSQL and PostGIS
Both are available via Homebrew on Mac

2. Download raw data
./download_raw_data.sh && ./remove_bad_rows.sh

The remove_bad_rows.sh script fixes two particular files that have a few rows with too many columns. See the "data issues" section below for more.

Note that the raw data is hundreds of GB, so it will take a while to download.

3. Initialize database and set up schema
./initialize_database.sh

4. Import taxi and FHV data
./import_trip_data.sh
./import_fhv_trip_data.sh

The full import process takes ~36 hours on a 2013 MacBook Pro with 16 GB of RAM.

5. Analysis
Additional Postgres and R scripts for analysis are in the analysis/ folder, or you can do your own!

Schema
trips table contains all yellow and green taxi trips. Each trip has a cab_type_id, which references the cab_types table and refers to one of yellow or green
fhv_trips table contains all for-hire vehicle trip records, including ride-hailing apps Uber, Lyft, Via, and Juno
fhv_bases maps fhv_trips to base names and "doing business as" labels, which include ride-hailing app names
nyct2010 table contains NYC census tracts plus the Newark Airport. It also maps census tracts to NYC's official neighborhood tabulation areas
taxi_zones table contains the TLC's official taxi zone boundaries. Starting in July 2016, the TLC no longer provides pickup and dropoff coordinates. Instead, each trip comes with taxi zone pickup and dropoff location IDs
central_park_weather_observations has summary weather data by date
Other data sources
These are bundled with the repository, so no need to download separately, but:

Shapefile for NYC census tracts and neighborhood tabulation areas comes from Bytes of the Big Apple
Shapefile for taxi zone locations comes from the TLC
Mapping of FHV base numbers to names comes from the TLC
Central Park weather data comes from the National Climatic Data Center
Data issues encountered
Remove carriage returns and empty lines from TLC data before passing to Postgres COPY command
Some raw data files have extra columns with empty data, had to create dummy columns junk1 and junk2 to absorb them
Two of the yellow taxi raw data files had a small number of rows containing extra columns. I discarded these rows
The official NYC neighborhood tabulation areas (NTAs) included in the census tracts shapefile are not exactly what I would have expected. Some of them are bizarrely large and contain more than one neighborhood, e.g. "Hudson Yards-Chelsea-Flat Iron-Union Square", while others are confusingly named, e.g. "North Side-South Side" for what I'd call "Williamsburg", and "Williamsburg" for what I'd call "South Williamsburg". In a few instances I modified NTA names, but I kept the NTA geographic definitions
The shapefile includes only NYC census tracts. Trips to New Jersey, Long Island, Westchester, and Connecticut are not mapped to census tracts, with the exception of the Newark Airport