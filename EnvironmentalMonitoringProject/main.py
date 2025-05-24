import sys
import os
import random
from datetime import datetime

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flaskr.utils.config.configurator import read_yaml_conf
from flaskr.utils.logging.logger import set_root_logger
from mvc.models.authenticator import user_authenticator, user_register, user_reset
from mvc.models.data_loader import measurements_fetcher, date_selection_measurements_fetcher
from mvc.visualize.visualizor import plot_measurements
from utils.dbconnection.dbconnector import db_source_connect

# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.abspath(__file__))
# root_dir = os.path.join(os.path.dirname(__file__), 'flaskr', 'mvc')
sys.path.append(root_dir)
# Init Flask app variable
app = Flask(__name__, static_url_path='', static_folder='flaskr\\static', template_folder='flaskr\\templates')
# Set secret key
app.secret_key = 'SDDDADDAS@#5445412!'  # Replace 'your_secret_key_here' with your actual secret key


# Function to convert timestamp values to datetime format
def convert_timestamp(timestamp_ms):
    timestamp_sec = timestamp_ms.timestamp()
    return datetime.utcfromtimestamp(timestamp_sec).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/streaming', methods=['GET'])
def get_streaming():
    return render_template('streaming.html')


@app.route('/api/data', methods=['GET'])
def get_api_data():
    df1, df2, df3, df4, df5 = measurements_fetcher(logger, configuration)
    df5['timestamp'] = df5['timestamp'].apply(convert_timestamp)
    # Convert DataFrame to JSON
    json_data = df5.to_json(orient='records')
    return json_data


@app.route('/search', methods=['POST'])
def search():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def search()...\n")
    if request.method == 'POST':
        start_time = request.form.get('start-time')
        end_time = request.form.get('end-time')
        if start_time is None or end_time is None:
            return render_template('measurements.html', error=2223)
        else:
            # Render the same page, measurements but with the new 3 plots.
            df1, df2, df3, df4 = date_selection_measurements_fetcher(logger, configuration, start_time, end_time)
            if df1 is None:
                return render_template('measurements.html', error=2222)
            else:
                graph_json1, graph_json2, graph_json3, graph_json4 = plot_measurements(logger, df1, df2, df3, df4)
                return render_template('measurements.html', graphJSON1=graph_json1,
                                       graphJSON2=graph_json2, graphJSON3=graph_json3,
                                       graphJSON4=graph_json4)
    else:
        return jsonify('Error. Only POST action allowed..'), 401


@app.route('/measurements')
def measurements():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def measurements()...\n")
    df1, df2, df3, df4, df5 = measurements_fetcher(logger, configuration)
    if df1 is None:
        return render_template('measurements.html', error='DB ERROR. NO PLOTS.')
    else:
        graph_json1, graph_json2, graph_json3, graph_json4 = plot_measurements(logger, df1, df2, df3, df4)
        return render_template('measurements.html', graphJSON1=graph_json1,
                               graphJSON2=graph_json2, graphJSON3=graph_json3,
                               graphJSON4=graph_json4)


@app.route('/menu')
def menu():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def menu()...\n")
    return render_template('index.html')


@app.route('/information')
def information():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def information()...\n")
    return render_template('information.html')


@app.route('/reset_pass_user', methods=['GET', 'POST'])
def reset_pass_user():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def reset_pass_user()...\n")
    if request.method == 'POST':
        # Call user_register method to check if user already exists before registering him
        result = user_reset(logger, configuration, request, session)
        if result == 1:
            return render_template('reset.html', error=1)
        elif result == 2:
            return render_template('register.html',
                                   error="Authentication cannot be completed due to database connection error.")
        elif result == 3:
            return render_template('login.html')  # Password reset successful
        elif result == 4:
            return render_template('reset.html', error=2)
    else:
        return jsonify('Error. Only POST action allowed..'), 401


@app.route('/reset_pass', methods=['GET', 'POST'])
def reset_pass():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def reset_pass()...\n")
    return render_template('reset.html', error=0)


@app.route('/register_user', methods=['POST'])
def register_user():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def register_user()...\n")
    if request.method == 'POST':
        # Call user_register method to check if user already exists before registering him
        result = user_register(logger, configuration, request, session)
        if result == 1:
            return render_template('register.html', error=1)
        elif result == 2:
            return render_template('register.html',
                                   error="Authentication cannot be completed due to database connection error.")
        elif result == 3:
            return render_template('register.html', error=3)
        elif result == 4:
            return render_template('login.html')  # Registration successful
    else:
        return jsonify('Error. Only POST action allowed..'), 401


@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def register()...\n")
    return render_template('register.html', error=0)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def authenticate()...\n")
    result = user_authenticator(logger, configuration, request, session)
    if result == 1:
        return jsonify('Error. Only POST action allowed..'), 401
    elif result == 2:
        return render_template('login.html', error=1)
    elif result == 3:
        return render_template('login.html',
                               error="Authentication cannot be completed due to database connection error.")
    elif result == 4:
        return render_template('index.html')  # Authentication successful
    elif result == 5:
        return render_template('login.html', error=2)


@app.route('/', methods=['GET', 'POST'])
def login():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def login()...\n")
    if request.method == 'POST' or request.method == 'GET':
        return render_template('login.html', error=0)


@app.route('/logout')
def logout():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def logout()...\n")
    # Remove user data from session
    session.pop('user', None)
    return redirect(url_for('login'))


# Before each request, check if user is logged in
@app.before_request
def before_request():
    logger.info('<' + os.path.basename(__file__) + '>' + " - def before_request()...\n")
    if request.endpoint in ['login', 'logout', 'static', 'authenticate', 'register', 'register_user', 'reset_pass',
                            'reset_pass_user']:
        return
    # Check if users is logged in
    if 'user' not in session:
        return redirect((url_for('login')))


if __name__ == "__main__":
    # First action: Set root logger
    logger = set_root_logger()
    logger.info('<' + os.path.basename(__file__) + '>' + " - Starting application...\n"
                                                         "=============================="
                                                         "================================"
                                                         "========================================\n")
    # Second action: Read the yaml configuration file
    configuration = read_yaml_conf(logger)
    # Finally, run flask service in the background!
    app.run(host='0.0.0.0', port=configuration['web_info']['flask']['port'], debug=True)

