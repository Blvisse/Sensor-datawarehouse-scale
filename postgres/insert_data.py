import pandas as pd
import numpy as np
import psycopg2
from tqdm import tqdm as tq

from psycopg2 import OperationalError, errorcodes, errors
import os
import sys


print("loaded libraries")

try:
    for i in tq(range(100), desc="Connecting to postgres"):
        pass
    connection = psycopg2.connect(database="postgres", user="postgres", password="")
    connection.autocommit = True
    print("Successfully connected to postgres database")
except OperationalError as e:
    print("Failed to connect to postgres db \n")
    print("Check credentials and retry")
    print ("Safely exiting system")
    sys.exit(1)

#create cursor for purpose of querying the db 
cursor = connection.cursor()

print("Rdaing dat file....")
data = pd.read_csv('../sensorscale/data/station_summary.csv')
for i in tq(range(len(data)), desc="Reading data"):
    pass

print("Finished reading data...")


print("Inserting data into database...")
try:
    for row in data.itertuples():
        print(row)
        cursor.execute('''

            INSERT INTO sensor_data.station_test (ID,flow_99,flow_max,flow_median,flow_total,n_obs)
            VALUES(%s,%s,%s,%s,%s,%s);
            
            
        ''',
            (row.ID, row.flow_99, row.flow_max, row.flow_median, row.flow_total, row.n_obs)
            )
    connection.commit()
    print("Successfully populated tables")
except errors.UndefinedTable:
    print("The table you are inserting data to doesn't exist..")
    print("Closing db connection")
    connection.close()

    print("Exiting...")
    sys.exit(1)
print("closing connection")
connection.close()
