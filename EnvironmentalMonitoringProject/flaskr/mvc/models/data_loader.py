import os
from datetime import timedelta, datetime
import pandas as pd
from utils.dbconnection.dbconnector import db_source_connect


def measurements_fetcher(logger, configuration):
    logger.info('<' + os.path.basename(__file__) + '>' + "- def measurements_fetcher(logger, configuration)...\n")
    # Now, make 3 select queries from NOW and on week before.
    conn = db_source_connect(logger, configuration)
    df1 = df2 = df3 = None
    if conn is None:
        logger.error('<' + os.path.basename(
            __file__) + '>' + " - def measurements_fetcher(logger, configuration)()...\n" + "DB ERROR.. \n")
        return df1, df2, df3
    else:
        cursor = conn.cursor()
        # Calculate the date one week ago
        one_week_ago = datetime.now() - timedelta(days=7)
        cursor.execute("SELECT timestamp, co2 FROM public.measurements WHERE timestamp >= %s", (one_week_ago,))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df1 = pd.DataFrame(results, columns=['timestamp', 'co2'])
        # -------------------------------------------------------
        cursor.execute("SELECT timestamp, o2 FROM public.measurements WHERE timestamp >= %s", (one_week_ago,))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df2 = pd.DataFrame(results, columns=['timestamp', 'o2'])
        # -------------------------------------------------------
        cursor.execute("SELECT timestamp, humidity FROM public.measurements WHERE timestamp >= %s", (one_week_ago,))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df3 = pd.DataFrame(results, columns=['timestamp', 'humidity'])
        # -------------------------------------------------------
        cursor.execute("SELECT timestamp, no2 FROM public.measurements WHERE timestamp >= %s", (one_week_ago,))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df4 = pd.DataFrame(results, columns=['timestamp', 'no2'])
        # -------------------------------------------------------
        cursor.execute("SELECT timestamp, co2, humidity, o2, no2 FROM public.measurements WHERE timestamp >= %s", (one_week_ago,))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df5 = pd.DataFrame(results, columns=['timestamp', 'co2', 'humidity', 'o2', 'no2'])
        # Close the cursor and connection
        # Close the cursor and connection
        cursor.close()
        conn.close()
        return df1, df2, df3, df4, df5


def date_selection_measurements_fetcher(logger, configuration, start_time, end_time):
    logger.info('<' + os.path.basename(__file__) + '>' +
                "- def date_selection_measurements_fetcher(logger, configuration)...\n")
    # Now, make 3 select queries based on the user input
    conn = db_source_connect(logger, configuration)
    df1 = df2 = df3 = None
    if conn is None:
        logger.error('<' + os.path.basename(
            __file__) + '>' + " - def measurements_fetcher(logger, configuration)()...\n" + "DB ERROR.. \n")
        return df1, df2, df3
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, co2 FROM public.measurements WHERE timestamp >= %s AND timestamp <= %s;", (start_time, end_time))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df1 = pd.DataFrame(results, columns=['timestamp', 'co2'])
        # -------------------------------------------------------
        cursor.execute("SELECT timestamp, o2 FROM public.measurements WHERE timestamp >= %s AND timestamp <= %s;", (start_time, end_time))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df2 = pd.DataFrame(results, columns=['timestamp', 'o2'])
        # -------------------------------------------------------
        cursor.execute("SELECT timestamp, humidity FROM public.measurements WHERE timestamp >= %s AND timestamp <= %s;", (start_time, end_time))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df3 = pd.DataFrame(results, columns=['timestamp', 'humidity'])
        # -------------------------------------------------------
        cursor.execute("SELECT timestamp, no2 FROM public.measurements WHERE timestamp >= %s AND timestamp <= %s;",
                       (start_time, end_time))
        # Fetch the results
        results = cursor.fetchall()
        # Convert the results into a DataFrame
        df4 = pd.DataFrame(results, columns=['timestamp', 'no2'])
        # Close the cursor and connection
        cursor.close()
        conn.close()
        return df1, df2, df3, df4
