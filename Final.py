import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

#
# Name: Your Name
# CS230: Section SN5
# Data: Earthquake
# URL: https://share.streamlit.io/timothytat/timothy-tat/main/Final.py
#
# Description: This program ... (a few sentences about your program and the queries and charts)
#

MAPKEY = "pk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DApk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DA"

data = pd.read_csv("earthquakes_us_20201123.csv")
data = data[['time', 'latitude', 'longitude', 'mag', 'place', 'locationSource']]
linedata = data[['time', 'latitude', 'longitude', 'mag', 'place', 'locationSource']]

for index, row in data.iterrows():  # cleaned data to only have the state
    z = row["place"]
    if z.find(',') > 0:
        state = z[z.find(',') + 2:]
        data.at[index, 'place'] = state

for index, row in data.iterrows():  # cleaned data to only have the month the earthquake occurred in
    z = row["time"]
    month = z[z.find('-') + 1:z.find('-') + 3]
    data.at[index, 'time'] = month

top = data.sort_values('mag', ascending=False).head(10)
data["scaled_radius"] = data["mag"] / data["mag"].max() * 50

for index, row in linedata.iterrows():  # cleaned data to only have the month the earthquake occurred in
    z = row["time"]
    lmonth = z[0:z.find('T')]
    linedata.at[index, 'time'] = lmonth


def mapping(d, color):  # function takes in 2 parameters and returns a map
    view_state = pdk.ViewState(
        latitude=top["latitude"].mean(),
        longitude=top["longitude"].mean(),  # Used a mean (requirement)
        zoom=1,
        pitch=0)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=d,
                       get_position='[longitude, latitude]',
                       get_radius='scaled_radius',
                       radius_scale=2,
                       radius_min_pixels=3,
                       radius_max_pixels=400,
                       get_color=[.8 * color, .1 * color, 0],
                       pickable=True
                       )
    tool_tip = {"html": "Magnitude:<br/> <b>{mag}</b> ",
                "style": {"backgroundColor": "crimson",
                          "color": "white"}
                }
    map2 = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        mapbox_key=MAPKEY,
        layers=layer1,
        tooltip=tool_tip
    )
    return map2


#  setting up the streamlit display
st.set_page_config(layout="wide")
st.header("Final Python Project")
col1, col2 = st.beta_columns(2)

col1.subheader("Top 10 locations with most earthquakes:")
col1.bar_chart(data['place'].value_counts().head(10))

col2.subheader('All Earthquakes for the month:')
months = ["09", "10", "11"]
eq_months = col2.radio("Select a month:",
                       months)  # a radio button to change the display of earthquakes on the map by months
y = col2.slider("Color", 0.0, 255.0, 100.0)
data.mon = data.loc[data.time == eq_months]
col2.pydeck_chart(mapping(data.mon, y))

col1.subheader("Time series of number of earthquakes:")
col1.line_chart(linedata['time'].value_counts())

col1.subheader("Pie chart of centers and percent of earthquakes located:")
fig, ax = plt.subplots()
ax.pie(data['locationSource'].value_counts(), autopct='%1.1f%%', labels=data.locationSource.unique())
col1.pyplot(fig)

if col2.button(
        'Top 10 Largest Magnitude (Hover over to see magnitude)'):  # button displaying the top ten earthquakes based on magnitude
    st.pydeck_chart(mapping(top, 200))
    st.write(top.head(10))
