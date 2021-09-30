from airflow import DAG
from random import randint
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import logging
import pandas as pd

logging.basicConfig(
    filename='../logs/store.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)
print("Done Loading libraries")
logging.info("Done loading libraries")


def best_data(ti):
    # accuracies=ti.xcom_pull(task_ids=['data_get','data_get_2','data_get_3'])
    # best_accuracy=max(accuracies)
    # if(best_accuracy >8):
    #     return 'accurate'
    print("Datasets have been loaded into the system")


def migrate_stations():
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

                    INSERT INTO sensor_data.station_summary (ID,flow_99,flow_max,flow_median,flow_total,n_obs)
                    VALUES(%(ID)s,%(flow_99)s,%(flow_max)s,%(flow_median)s,%(flow_total)s,%(n_obs)s);
                    
                    
                ''', row)
            except Exception as e:
                print(e)

    print("Done..")



def store_stations_data():
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


    mysql_cursor.execute("SELECT * FROM i80_stations")
    print("Migrating stations table to postgres database....")
    for i in tq(range(10), desc="Migrating to postgres"):
        for row in mysql_cursor:
            try:
                post_cursor.execute(
                    '''
                    INSERT INTO sensor_data."I80_stations"(ID,fwy,dir,district,county,city,state_pm,abs_pm,latitude,longitude,length,type,lanes,name,user_id_1,user_id_2,user_id_3,user_id_4)
                    VALUES (%(ID)s,%(fwy)s,%(dir)s,%(district)s,%(district)s,%(city)s,%(state_pm)s,%(abs_pm)s,%(latitude)s,%(longitude)s,%(length)s,%(type)s,%(lanes)s,%(name)s,%(user_id_1)s,%(user_id_2)s,%(user_id_3)s,%(user_id_4)s);

                    ''', row)

            except Exception as e:
                print(e)

    mysql_cursor.execute("SELECT * FROM i80_median")
    print("querying median table in sql")

    print("Migrating median table to postgres database...")
    for i in tq(range(10), desc="Migrating to postgres"):
        for row in mysql_cursor:

            try:

                post_cursor.execute(
                    '''

                    INSERT INTO sensor_data.tests (ID,weekday,hour,minute,second,flow1,occupancy1,mph1,flow2,occupancy2,mph2,flow3,occupancy3,mph3,flow4,occupancy4,mph4,flow5,occupancy5,mp5,totalflow)
                    VALUES(%(ID)s,%(weekday)s,%(hour)s,%(minute)s,%(second)s,%(flow1)s,%(occupancy1)s,%(mph1)s,%(flow2)s,%(occupancy2)s,%(mph2)s,%(flow3)s,%(occupancy3)s,%(mph3)s,%(flow4)s,%(occupancy4)s,%(mph4)s,%(flow5)s,%(occupancy5)s,%(mp5)s,%(totalflow)s);
                    
                    
                ''', row)
            except Exception as e:
                print(e)

    print("Done..")

  

with DAG("fetch_data_dag",
         start_date=datetime(2021, 1, 1),
         schedule_interval="@daily",
         catchup=False) as dag:

    fetch_data_1 = PythonOperator(
        task_id="data_get",
        python_callable=store_stations_data,
    )
    fetch_data_2 = PythonOperator(
        task_id="data_get_2",
        python_callable=migrate_stations,
    )

    best_data = BranchPythonOperator(task_id="select_model",
                                     python_callable=best_data)
    # accurate=BashOperator(
    #     task_id="accurate",
    #     bash_command="echo 'accurate'"
    # )
    # inacurate=BashOperator(
    #     task_id="inacurate",
    #     bash_command="echo 'inacurate'"
    # )

[fetch_data_1, fetch_data_2] >> best_data
