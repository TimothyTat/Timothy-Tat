import numpy as np
import streamlit as st
import pydeck as pdk
import pandas as pd
import mapbox as mb
import matplotlib.pyplot as plt

MAPKEY = "pk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DApk.eyJ1IjoiY2hlY2ttYXJrIiwiYSI6ImNrOTI0NzU3YTA0azYzZ21rZHRtM2tuYTcifQ.6aQ9nlBpGbomhySWPF98DA"


data = pd.read_csv("earthquakes_us_20201123.csv")
data = data[['time', 'latitude', 'longitude', 'mag', 'place', 'locationSource']]

for index, row in data.iterrows():  # cleaned data to only have the state
    z = row["place"]
    if z.find(',') > 0:
        state = z[z.find(',') + 2:]
        data.at[index, 'place'] = state

for index, row in data.iterrows():  # cleaned data to only have the month the earthquake occurred in
    z = row["time"]
    month = z[z.find('-') + 1:z.find('-') + 3]
    data.at[index, 'time'] = month

print(data['time'])
top = data.sort_values('mag', ascending=False).head(10)
print(top['mag'])
data["scaled_radius"] = data["mag"] / data["mag"].max() * 50
print(data['scaled_radius'])

#  setting up the streamlit display

st.header("Final Python Project")
st.subheader("Top 10 locations with most earthquakes:")
st.bar_chart(data['place'].value_counts().head(10))


if st.button('Top 10 Largest Magnitude'):  # button displaying the top ten earthquakes based on magnitude
    view_state = pdk.ViewState(
    latitude=top["latitude"].mean(),
    longitude=top["longitude"].mean(),
    zoom=1,
    pitch=0)
    top["scaled_radius"] = top["mag"]/top["mag"].max() *400
    layer1 = pdk.Layer('ScatterplotLayer',
                  data=top,
                  get_position='[longitude, latitude]',
                  get_radius='scaled_radius',
                  radius_scale =2,
                  radius_min_pixels= 10,
                  radius_max_pixels = 400,
                  get_color=[255,0,255],
                  pickable=True
                  )
    tool_tip = {"html": "Magnitude:<br/> <b>{mag}</b> ",
            "style": { "backgroundColor": "crimson",
                        "color": "white"}
          }
    map2 = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    mapbox_key=MAPKEY,
    layers= layer1,
    tooltip= tool_tip
    )
    st.pydeck_chart(map2)
    st.write(top)

st.subheader('All Earthquakes for the month:')
months = ["09", "10", "11"]
eq_months = st.radio("Select a month:", months)  # a radio button to change the display of earthquakes on the map by months
data.mon = data.loc[data.time == eq_months]
st.map(data.mon)

# st.subheader("Choose which state to look at:")
# multi_state = data['place'].unique()
# print(multi_state)
# multi_state_select = st.multiselect('Select state:', multi_state, default=['CA'])
# data_state = data.loc(data.place in multi_state_select)
# st.map(data_state)

st.subheader("Bar chart of number of earthquakes by month:")
st.bar_chart(data['time'].value_counts())

st.subheader("Pie chart of centers and percent of earthquakes located:")
fig, ax = plt.subplots()
ax.pie(data['locationSource'].value_counts(), autopct='%1.1f%%', labels=data.locationSource.unique())
st.pyplot(fig)
