import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="Best Price per Rental Type",
    page_icon="👋",
)

st.title('Best Prices by Type of Rental')

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
In this section, I want to figure out what areas of the city have the best price per rental type. My concept for this section is to have a two-dimensional map. We can use a heatmap or hexagonal map to define the average property value, and then a scatterplot or something similar to show points for each type of rental on top of that.
"""
)

# Display our chart
st.markdown(
"""
### Property Value Map with Property Types
This map allows us to select the type of property we want to look for in the selection box below.

Also, please note that the heatmap on this chart is a neurtal blue. The deeper the blue color, the more expensive property values are.
"""
)

choice = st.selectbox("Choose a property type", ["Full home/apartment", "Hotel", "Private room"])

if choice == 'Full home/apartment':
    data_filter = data[(data.room_type == "Entire home/apt")]
elif choice == 'Hotel':
    data_filter = data[(data.room_type == "Hotel room")]
else:
    data_filter = data[(data.room_type == "Private room")]

view = pdk.data_utils.compute_view(data[["longitude", "latitude"]])
view.pitch = 55
view.bearing = 60
view.zoom = 10

elevation_calc = lambda x: x.availability_365 / 365

data = data.assign(elevation = elevation_calc)

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=view,
    layers=[
        pdk.Layer(
            'HeatmapLayer',
            data=data,
            opacity=0.4,
            get_position='[longitude, latitude]',
            get_weight="price",
            aggregation=pdk.types.String("MEAN"),
            color_range=COLOR_BREWER_BLUE_SCALE,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data=data_filter,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=10,
            radius_min_pixels=0,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position='[longitude, latitude]',
            get_fill_color=[255, 140, 0],
        )
    ],
))

st.markdown(
"""
Now, we can use this chart to look for certain types of properties in high or low value areas.
"""
)