# '''
# This script migrates data from the sql to postgres database

# '''

# import pandas as pd
# import pyodbc
# import os
# import re
# from sqlalchemy import create_engine

# database_name = 'sensor_datawarehouse'
# mssqlserver_servername = 'localhost'

# mssqlserver_uri = f"mssql+pyodbc://root:root@{mssqlserver_servername}/{database_name}?driver=SQL+Server"
# mssqlserver_engine = create_engine(mssqlserver_uri)

# print(mssqlserver_engine)

# postgres_uri = f"postgres+psycopg2://postgres:root@localhost:5432/{database_name}"
# postgres_engine = create_engine(postgres_uri)

# print(postgres_engine)

# mssqlserver_table_query = """

#     SELECT
#           t.name AS table_name
#         , s.name AS schema_name
#     FROM sys.tables t
#     INNER JOIN sys.schemas s
#     ON t.schema_id = s.schema_id

#     UNION

#     SELECT
#           v.name AS table_name
#         , s.name AS schema_name
#     FROM sys.views v
#     INNER JOIN sys.schemas s
#     ON v.schema_id = s.schema_id

#     ORDER BY schema_name, table_name;

# """

# mssqlserver_connection = mssqlserver_engine.connect()

# mssqlserver_tables = mssqlserver_connection.execute(mssqlserver_table_query)
# mssqlserver_tables = mssqlserver_tables.fetchall()
# mssqlserver_tables = dict(mssqlserver_tables)

# mssqlserver_schemas = set(mssqlserver_tables.values())

# mssqlserver_connection.close()

import os
import sys
import mysql.connector
import psycopg2
# import MySQLdb
from mysql.connector import Error
from tqdm import tqdm as tq
from psycopg2 import OperationalError, errorcodes, errors
import os
import sys

try:
    conn_mysql = mysql.connector.connect(host='localhost',
                                         user='root',
                                         password='root',
                                         database='sensor_datawarehouse')
    print("connected to the mysql database")
    mysql_cursor = conn_mysql.cursor(dictionary=True)

except Error as e:

    print(e)

#postgres connection

try:
    for i in tq(range(100), desc="Connecting to postgres"):
        pass
    post_connection = psycopg2.connect(database="postgres",
                                       user="postgres",
                                       password="")
    post_connection.autocommit = True
    print("Successfully connected to postgres database")
    post_cursor = post_connection.cursor()
except OperationalError as e:
    print("Failed to connect to postgres db \n")
    print("Check credentials and retry")
    print("Safely exiting system")
    sys.exit(1)

#sql query
print("querying summary table in sql")
mysql_cursor.execute("SELECT * FROM summary_table")

print("Migrating summary table to postgres database...")
for i in tq(range(10), desc="Migrating to postgres"):
    for row in mysql_cursor:
        # print(row)
        try:

            post_cursor.execute(
                '''

                INSERT INTO sensor_data.migration_test (ID,flow_99,flow_max,flow_median,flow_total,n_obs)
                VALUES(%(ID)s,%(flow_99)s,%(flow_max)s,%(flow_median)s,%(flow_total)s,%(n_obs)s);
                
                
            ''', row)
        except Exception as e:
            print(e)

print("Done..")

##### we now migrate the rest of the tables
