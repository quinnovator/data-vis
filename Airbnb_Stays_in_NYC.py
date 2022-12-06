import streamlit as st

st.set_page_config(
    page_title="Airbnb Data in NYC",
    page_icon="👋",
)

st.sidebar.success("Select a visualization above.")

st.markdown(
"""
# Airbnb Stay Data in New York City
Welcome! This is my final project for Fundamentals of Data Visualization. In this project, I analyze
data from Inside Airbnb, an organization that open-sources datasets on Airbnb stays.

---

This project aims to answer a few questions about the dataset through visualization, which are listed here:

#### Question 1
> Which boroughs in New York have the most Airbnb rental activity?
We know that New York City is full of short term rentals, but which boroughs in the city have the most rental traffic? Additionally, we can dig deeper to find out if the areas with the most traffic are consistent with the areas that have the top-ranked short term rentals.

#### Question 2
> Which boroughs in New York have the best price per type of home (full home/apartment, hotel room, private room in house)?
While we already know that certain areas of the city are more expensive than others, can we identify the areas of the city that have the best prices per type of home?

#### Question 3
> Which Airbnb properties are earning the most revenue?
I'm curious about the proeprties that are earning the most revenue from our dataset.

---

This interactive visualization was made with Streamlit, which is a static-site generator that leverages Altair and other visualization tools in the background to create visualizations.

"""
)