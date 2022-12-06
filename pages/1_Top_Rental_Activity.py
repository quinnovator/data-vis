import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="Top Rental Activity Areas in NYC",
    page_icon="👋",
)

st.title('Top Rental Activity in NYC')

# Defining constants used in our visualization
DATA_URL = './listings.csv'

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.drop('license', axis=1, inplace=True)
    data.dropna(inplace=True)
    data = data[data['availability_365'] > 0]
    return data

# Load 15,000 observations into memory (lower this if performance is problematic)
data_load_state = st.text('Getting ready... please wait!')
data = load_data(10000)
data_load_state.empty()

# Explain my visualization
st.markdown(
"""
In this section, I want to answer the question about which boroughs in New York City have the most short-term rental traffic.
To do this, I will use Streamlit in conjunction with a library called Pydeck.
"""
)

# Display our chart
st.markdown(
"""
### Listing Heatmap in New York City
Here, we can see a heatmap of 10,000 randomly selected listings on the Airbnb platform in New York.
Even though this visualization makes it easy to see where most listings are, it doesn\'t answer our question about whether or not these rentals have the most traffic.
One component included in the dataset for us is the available nights per 365 days. In order to answer whether the number of listings correlates with availability nights, I will use a hexagon layer to add a thrid dimension to the heatmap.

The elevation of the map corresponds to the percentage of availability nights in New York. If we saw that the elevated portions of the graph where largely yellow (not red) this would indicate that the areas with the most listings don't neccessarily have the most traffic.
We don't see this trend. Instead, we can see that those variables appear to have some correlation.

This makes sense, since the areas with the most traffic are likely where investors will create rentals.

As a result, we now have an interactive heatmap of areas in New York City that see the most rental traffic.
"""
)

view = pdk.data_utils.compute_view(data[["longitude", "latitude"]])
view.pitch = 55
view.bearing = 60
view.zoom = 10

elevation_calc = lambda x: x.availability_365 / 365

data = data.assign(elevation = elevation_calc)

tooltip = {
    "text": "Night availability score: {elevationValue}",
}

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=view,
    tooltip=tooltip,
    layers=[        
        pdk.Layer(
            'HeatmapLayer',
            data=data,
            opacity=0.4,
            get_position='[longitude, latitude]'
        ),
        pdk.Layer(
            'HexagonLayer',
            data=data,
            radius=100,
            get_position='[longitude, latitude]',
            get_elevation="elevation",
            opacity=0.4,
            extruded=True,
            pickable=True,
            auto_highlight=True,
        ),

    ],
))
