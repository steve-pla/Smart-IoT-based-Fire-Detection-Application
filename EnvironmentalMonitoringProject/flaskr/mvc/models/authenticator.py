import os
from utils.dbconnection.dbconnector import db_source_connect


def user_authenticator(logger, configuration, request, session):
    logger.info('<' + os.path.basename(__file__) + '>' + "- def user_authenticator(logger, configuration, request, "
                                                         "session)...\n")
    if request.method == 'GET':
        return 1
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if username or password is empty
        if not username or not password:
            # Return JSON error message with status code 400 (Bad Request)
            return 2
        # open connection to PostgreSQL to check the user
        conn = db_source_connect(logger, configuration)
        if conn is None:
            logger.error('<' + os.path.basename(__file__) + '>' + " - def authenticate()...\n" + "DB ERROR.. \n")
            return 3
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.users WHERE user_email = %s AND password = %s", (username, password))
        row = cursor.fetchone()
        if row:
            session['user'] = row
            return 4
        # Close the cursor and the connection
        conn.cursor().close()
        conn.close()
        return 5


def user_register(logger, configuration, request, session):
    logger.info('<' + os.path.basename(__file__) + '>' + "- def user_register(logger, configuration, request, "
                                                         "session)...\n")
    # First, we check if user email and password are null from the html page
    username = request.form.get('username')
    password = request.form.get('password')
    # Check if username or password is empty
    if not username or not password:
        return 1
    # Then, we have to open DB connection to fetch all users info.
    conn = db_source_connect(logger, configuration)
    if conn is None:
        logger.error('<' + os.path.basename(__file__) + '>' + " - def user_register()...\n" + "DB ERROR.. \n")
        return 2
    cursor = conn.cursor()
    cursor.execute("SELECT user_email FROM public.users WHERE user_email = %s", (username,))
    row = cursor.fetchone()
    if row:
        # Email already exists, display error message
        return 3
    else:
        # Email doesn't exist, proceed with registration logic
        # (Insert user data into the database)
        insert_query = "INSERT INTO public.users (user_email, password) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, password))
        conn.commit()  # Commit the transaction after successful insertion
        # Set this user free to use APIs. Is now authenticated!
        # session['user'] = row
        # Close the cursor and the connection
        conn.cursor().close()
        conn.close()
        return 4


def user_reset(logger, configuration, request, session):
    logger.info('<' + os.path.basename(__file__) + '>' + "- def user_register(logger, configuration, request, "
                                                         "session)...\n")
    # First, we check if user email and password are null from the html page
    username = request.form.get('username')
    password = request.form.get('password')
    # Check if username or password is empty
    if not username or not password:
        return 1
    # Then, we have to open DB connection to fetch all users info.
    conn = db_source_connect(logger, configuration)
    if conn is None:
        logger.error('<' + os.path.basename(__file__) + '>' + " - def user_register()...\n" + "DB ERROR.. \n")
        return 2
    cursor = conn.cursor()
    cursor.execute("SELECT user_email FROM public.users WHERE user_email = %s", (username,))
    row = cursor.fetchone()
    if row:
        # Email already exists, the reset can be DONE!
        # Update user's password in the database
        update_query = "UPDATE public.users SET password = %s WHERE user_email = %s"
        cursor.execute(update_query, (password, username))
        conn.commit()
        return 3
    else:
        # Email doesn't exist, proceed with registration logic
        conn.cursor().close()
        conn.close()
        return 4

