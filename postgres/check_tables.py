
import pandas as pd
import numpy as np
import psycopg2
from tqdm import tqdm as tq

from psycopg2 import OperationalError, errorcodes, errors
import os
import sys

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
print(cursor)




cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'sensor_data'""")
for table in cursor.fetchall():
    print(table)