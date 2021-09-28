'''
This function creates a simple database in the postgres db
'''



import psycopg2
from tqdm import tqdm as tq
import os
import sys

#error handling library for postgres
from psycopg2 import OperationalError, errorcodes, errors


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


print("Creating query...")
query = ''' CREATE database sesnordata''';

try:
    cursor.execute(query)
    print("Successfully created database")
except errors.DuplicateDatabase:
    print("The database already exists")
    print("Safely exiting...")
    connection.close()
    sys.exit(1)

connection.close()
