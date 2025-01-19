import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from branca.colormap import linear
from branca.colormap import LinearColormap


df = pd.read_csv("Visualization_File.csv")


st.title("Home Rental Price Increase after LA Fires")
st.write(
    "This map shows the rental price increases for homes. "
    "Hover over a marker to see the address and percentage increase."
    "This was built using data collected by @bad_tenant."
    "Here is the link to the OG spreadsheet - https://docs.google.com/spreadsheets/d/1RXWxLqTyWvAuq8A0PgaBuWeEn_G6qTLyTZ8lzfNEaNw/edit?gid=314416722#gid=314416722"
)


m = folium.Map(location=[df["Latitude"].mean(),
               df["Longitude"].mean()], zoom_start=7.5)


colormap = LinearColormap(
    colors=["#f5f5f5", "#ff4d4d", "#990000", "#660000"],
    vmin=df["Percent_Increase"].min(),
    vmax=df["Percent_Increase"].max(),
)

colormap.caption = "Rental Price Increase (%)"
m.add_child(colormap)


for _, row in df.iterrows():
    color = colormap(row["Percent_Increase"])
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=10,
        color="black",
        weight=1,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        # popup=f"Address: {row['Full_Address']}<br /> Rent Increase: {row['Percent_Increase']}%",
        tooltip=f"Address: {row['Full_Address']} <br /> Rent Before: {row['Rental price (per month) BEFORE the increase']} <br />  Rent After: {row['Rental price (per month) AFTER the increase']} <br /> Rent Increase: {row['Percent_Increase']}%",
    ).add_to(m)

st_folium(m, width=700, height=500)
