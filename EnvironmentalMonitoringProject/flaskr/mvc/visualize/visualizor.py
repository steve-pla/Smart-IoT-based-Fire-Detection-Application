import json
import os
import plotly.express as px
import pandas as pd
import plotly.utils
import plotly.graph_objects as go
import plotly.figure_factory as ff
import psycopg2


def plot_measurements(logger, df1, df2, df3, df4):
    logger.info('<' + os.path.basename(__file__) + '>' + "- def plot_measurements(logger, df1, df2, df3)...\n")

    px.set_mapbox_access_token("pk.eyJ1Ijoic3BsYXN0cmFzIiwiYSI6ImNsMW05YTNsbjBnbG4zY29ieGRmb3htZWwifQ"
                               ".b9QDwexsmeYJN5Ug-L84mw")
    # Plot the 4 dataframes
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df1['timestamp'], y=df1['co2'], mode='lines', name='CO2'))
    fig1.update_layout(title='CO2 Over Time', xaxis_title='Timestamp', yaxis_title='CO2')
    fig1.update_layout(height=700, width=1100)
    # -----------------------------
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df2['timestamp'], y=df2['o2'], mode='lines', name='O2'))
    fig2.update_layout(title='Temperature Over Time', xaxis_title='Timestamp', yaxis_title='O2')
    fig2.update_layout(height=700, width=1100)
    # -------------------------------
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df3['timestamp'], y=df3['humidity'], mode='lines', name='Humidity -RH'))
    fig3.update_layout(title='Humidity Over Time', xaxis_title='Timestamp', yaxis_title='Humidity -RH')
    fig3.update_layout(height=700, width=1100)
    # -----------------------------
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df2['timestamp'], y=df4['no2'], mode='lines', name='NO2'))
    fig4.update_layout(title='Temperature Over Time', xaxis_title='Timestamp', yaxis_title='NO2')
    fig4.update_layout(height=700, width=1100)
    return (json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
            json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
            json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
            json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder))

