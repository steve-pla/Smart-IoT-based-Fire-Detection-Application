import os
import pandas as pd
import psycopg2


pd.options.mode.chained_assignment = None  # default='warn'


def db_source_connect(logger, configuration):
    logger.info('<' + os.path.basename(__file__) + '>' + " - def db_source_connect(logger, configuration)...\n")
    try:
        # "postgresql://username:password@your_sql_connection_url:port_number/database_name"
        # Establish a connection to the database
        conn = psycopg2.connect(dbname=configuration['data_source']['postgeqsql']['dbname'],
                                user=configuration['data_source']['postgeqsql']['dbuser'],
                                password=configuration['data_source']['postgeqsql']['password'],
                                host=configuration['data_source']['postgeqsql']['host'],
                                port=configuration['data_source']['postgeqsql']['port'])
        # Create a cursor object using the cursor() method
        # Return conn
        return conn
    except psycopg2.OperationalError as er:
        logger.error('<' + os.path.basename(__file__) + '>' + " - def db_source_connect(logger, configuration)...\n" + er)


