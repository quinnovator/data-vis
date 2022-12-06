import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Top Money Makers in NYC",
    page_icon="👋",
)

st.title('Top Revenue Generators in New York')

st.markdown(
    """
    In order to figure out NYC's best revenue drivers, I will use pandas to calculate the average price of a rental in a given area, then compare the price gotten by an individual rental to their average.
    
    I am plotting the results of this analysis using Altair.

    I should note that this analysis has brought my attention to some outliers in our dataset. There are some rentals that have extreme prices which are almost never rented out. I have excluded these observations so that our visualization is more readable.
    """
)

# Defining constants used in our visualization
DATA_URL = './listings.csv'

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
data = load_data(15000)
data_load_state.empty()

step = 0.2
to_bin = lambda x: np.floor(x / step) * step
data["latBin"] = to_bin(data.latitude)
data["lonBin"] = to_bin(data.longitude)
bin_avgs = data.groupby(["latBin", "lonBin"], as_index=False)['price'].mean()

avgs = {}

for lat, lon, price in bin_avgs.values:
    avgs[f'({str(round(lat, 4))}, {str(round(lon, 4))})'] = price

def get_avg(x):
    return avgs[f'({str(round(x.latBin, 4))}, {str(round(x.lonBin, 4))})']

data['avg_price'] = data.apply(lambda x: get_avg(x), axis=1)

data['relative_rate'] = data.apply(lambda x: round(x.price/x.avg_price, 2), axis=1)

data['occupied_nights'] = data.apply(lambda x: 365 - x.availability_365, axis=1)

data = data[data['relative_rate'] <= 15]

c = alt.Chart(data).mark_point().encode(
    x=alt.X('occupied_nights', axis=alt.Axis(title='Occupied Nights'), title='Occupied Nights'),
    y=alt.Y('price', axis=alt.Axis(title='Price per Night'), title="Price per Night"),
    size=alt.Size('relative_rate', title='Relative Rate'),
).properties(
    width=800,
    height=500
).interactive()

st.altair_chart(c)

st.markdown(
    """
    Great! Now, we can see which rentals are earning the most money relative to the others. I used a bubble plot becuase it allows us to show the relationship between occupied nights and price per night (there isn't much of one) as well as a way to tell which listings were the largest (rate-wise) relative to their competition.

    As we can see, some of these rentals toward the top-middle and top-right of the chart are sold out more than 50 percent of the year, and sometimes going for almost 14 times the price of their competitors. Wow!
    """
)