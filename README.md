[![GitHub issues](https://img.shields.io/github/issues/Blvisse/Sensor-datawarehouse-scale?style=for-the-badge)](https://github.com/Blvisse/Sensor-datawarehouse-scale/issues)
[![GitHub forks](https://img.shields.io/github/forks/Blvisse/Sensor-datawarehouse-scale?style=for-the-badge)](https://github.com/Blvisse/Sensor-datawarehouse-scale/network)
[![GitHub license](https://img.shields.io/github/license/Blvisse/Sensor-datawarehouse-scale?style=flat-square)](https://github.com/Blvisse/Sensor-datawarehouse-scale)
# Sensor-Data-Warehouse
## Background
With increasing size,compleity and demand for data there is need for proper data piplines to ease data retrival. Traditional ETL models are falling behind to modern data problems as it increases in size and need for real-time data.

The project aims to create a proper data-pipeline that uses data from sensors collected on I80 highway, and through this carry out processing and delivering a report on the data

Our previous data pipeline stack featured MySQL, airflow, dbt and redash, this integrated to create a seamless data pipeline. We however need to upgrade and compare scalable technologies to ensure that our data pipeline can handle a through beating. We used Postgres instead of MySQL and superset instead of redash



## Technologies used
1. Apache-Airflow
2. Postgres
3. DBT
4. Superset

## Folder structure
1. airflow: This folder contains airflow setup and dag files used to periodically insert data into the datawarehouse
2. python: Dockerfile containing a dbt image
3. env: virtual environment with superset installation
4. postgres: contains migration scripts and query manipulation
5. sensorscale: dbt instance of our data
6. superset: docker file image and superset files

## Installation requirements
The project is dockerrized and can be launched by running 

``` docker-compose up ```

The services have been assigned different port for accessing to access

dbt: ``` localhost:8080 ```

airflow: ``` loclhost:8001 ```

postgres: ``` localhost:5432 ```

superset: ``` localhost:8088 ```

### dbt
This database build tool is a powerful library that we shall use to carry out data trabsformation. To use it :
1. Navigate to the sensor_warehouse folder 
2. run the following command
3. ``` docker-compose up ``` 
4. To check if dbt is succefully installed run ``dbt version``
7. check to see that the installation didn;t bring any errors 
8. run `` dbt debug `` 
9. To run specified tests run `` dbt tests ``

#### Acessing dbt
Dbt credentials are set to 
Username: admin
paswword: admin

### view lineage graph
To view the lineage graph and dependancies between data run ```dbt generate docs```

### airflow

Airflow is used to schedule jobs. It creates an updated stream of data into our warehouse
1. Navigate to the airflow folder
2. run `` docker-compose up ``

### Accessing airflow
airflow credentails
username:admin
password:admin

### Postgres

Postgres is an open source, object-relational database management system. The previous stack used sql which is a relational database management system which means the database is based on the relational model, tables have at least one relational to another table. The ORDBMS has the qualities the RDBMS and adds on the object oriented aspect such as objects, classes and inheritance.

### Superset
Apache superset is an open-source software cloud-native application for data exploration and data visualization able to handle data at scale.

