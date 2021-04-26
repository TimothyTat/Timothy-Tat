import numpy as np
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

# streamlit run C:/Users/timot/Desktop/School/MA346/Final_Project_TimothyTat.py --server.port 550
pet = pd.read_csv("pet_data.csv")
st.set_page_config(layout="wide")
st.header("Final Data Science Project")
col1, col2 = st.beta_columns(2)

# I want to be able to create a choropleth map based on the percent of the population that owns a pet in each state. This
# will help us visualize which states have more pet owners and which ones have less.

fig = px.choropleth(pet, locations='State2', color='percAllPets', locationmode='USA-states', scope='usa',
                    hover_name="State", title='Map of Pet Ownership')
col1.plotly_chart(fig)

fig3 = px.choropleth(pet, locations='State2', color='percDogOwners', locationmode='USA-states', scope='usa',
                     hover_name="State", title='Map of Dog Ownership')
col1.plotly_chart(fig3)

fig4 = px.choropleth(pet, locations='State2', color='percCatOwners', locationmode='USA-states', scope='usa',
                     hover_name="State", title='Map of Cat Ownership')
col1.plotly_chart(fig4)

# As you can see from the choropleth the brighter the color (Towards yellow) the higher the percentage of the population
# owns a pet. From the map we can see that Wyoming has a very high pet owner percentage while a state like California has
# a low one.

# As a test, I wanted to see if there was a difference in the proportion of Dog owners to the proportion of Cat owners
# This calls for a difference in proportion test, using the mean proportions of both categories and an alpha of .05
col2.subheader("Is there a difference between the ownership of Dogs and Cats? (Difference in Proportions Test)")
col2.latex("Ho: P1 - P2 = 0 \quad Ha: P1 - P2 != 0")
col2.latex("Z = (P1-P2) / [P(1-P)(1/n1 + 1/n2)]")
mean_dog = pet["percDogOwners"].mean()
mean_cat = pet["percCatOwners"].mean()


# This is a function to calculate the difference in proportion.
def diffpop(p1, p2, n1, n2):
    p = (p1 + p2) / 2
    return (p1 - p2) / (((p * (1 - p)) * ((1 / n1) + (1 / n2))) ** .5)


z = diffpop(mean_dog, mean_cat, 48, 47)
col2.latex("P1 = " + str(mean_dog) + "\quad n1 = 48")
col2.latex("P2 = " + str(mean_cat) + "\quad n2 = 47")
col2.latex("Z = " + str(z) + "\quad Critial Value = 1.645")
col2.write("Since the Z score is not more extreme than the critial value of 1.645, Therefore we do not reject the "
           "null hypothesis and have no evidence of there being a difference in the proportion of Dog and Cat owners.")
# From the difference of proportions test, we find that there is no evidence of there being a difference in ownership of Dogs and Cats.

# Instead of looking at map there should be another way to see the states with the highest pet ownership.
fig2 = px.bar(pet, x='State', y='percAllPets')
fig2.update_layout(uniformtext_mode='show')
col2.plotly_chart(fig2)
# By using a bar chart, we can easily see the differences in the proportions between the states.

# Given a range of percentages, we want to narrow down which states are within that range.
ownership = col2.slider("States within this range of pet ownership", min_value=(pet['percAllPets'].min()),
                        max_value=(pet['percAllPets'].max()),
                        value=(float(pet['percAllPets'].min() - .01), float(pet['percAllPets'].max() + .01)))
col2.write(pet[(ownership[1] > pet['percAllPets']) & (pet['percAllPets'] > ownership[0])])
# Utilizing the slider tools of streamlit, we can use conditions to narrow down the states, based off the user moving the slider.

st.subheader("Map of animal shelters")
# Taking a sample from the large dataset of animal shelters. We want to put the location on the map and the name of the shelter
MAPKEY = "pk.eyJ1IjoiYXlvaXR6ZmFpbnQiLCJhIjoiY2tueTI4YWZvMTU0MDJ2bzI3Z2Vua3Y3MSJ9.K4IGSpHqTVBvsD0cBVqqOQ"
shelters = pd.read_csv("petfinder_shelters.csv")
sample = shelters.sample(250)

# We are setting up where to initially view the world map, taking the mean of the longitude and latitude, we get a centered initial view state.
view_state = pdk.ViewState(
    latitude=sample["latitude"].mean(),
    longitude=sample["longitude"].mean(), zoom=3.25)
# To plot the longitudes and latitudes of the data, we use a Scatterplot method, which puts points on the map based on their longitude and latitude
# Similar to a scatterplot.
layer1 = pdk.Layer(type='ScatterplotLayer',
                   data=sample,
                   get_position='[longitude, latitude]',
                   get_radius=17500,
                   get_color=[0, 0, 255],
                   pickable=True
                   )
# When clicking on one of the dots, we want to display information about it, therefore we want to know the name of the shelter that is being selected
tool_tip = {"html": "Name:<br/> <b>{name}</b> ",
            "style": {"backgroundColor": "crimson",
                      "color": "white"}
            }
map1 = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=layer1,
    tooltip=tool_tip
)

st.pydeck_chart(map1)
# This map is interactive, where you can click on the dot to show the name of the shelter, it also takes a random sample of shelters, therefore it is different everytime it refreshes.
