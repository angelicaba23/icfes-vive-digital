""" ---- DASHBOARD DS4A PROJECT ---- """

import datetime
import random
import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px  
import pydeck as pdk



# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="DS4A DASHBOARD", page_icon=":chart:")

# LOAD DATA ONCE
@st.experimental_singleton
def load_data():
    data = pd.read_csv(
        ".csv",
        names=[
            "lat",
            "lon",
        ],  # specify names directly since they don't change
        skiprows=1,  # don't read header since names specified directly
        usecols=[0, 1, 2],  # doesn't load all columns
        parse_dates=[
            ""
        ],  # set as datetime instead of converting after the fact
    )

    return data




# FUNCTION FOR MAPS
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["longitude", "latitude"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )


# FILTER DATA FOR A SPECIFIC HOUR, CACHE
@st.experimental_memo
def filterdf(df, hour_selected):
    return df[df["date/time"].dt.hour == hour_selected]


# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.experimental_memo
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# STREAMLIT APP LAYOUT
#data = load_data()


#TITLE OF THE PAGE
st.title("NAME OF THE PROJECT")

#INFO OF THE PROJECT
st.write(
    """
##
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin sagittis pellentesque orci, ut sagittis tortor ullamcorper in. Etiam erat est, egestas in consectetur id, pellentesque at sem. Praesent ligula magna, tincidunt at lorem sit amet, malesuada rhoncus quam. Vivamus elementum diam dui, nec mollis velit molestie ac. Ut vel maximus tortor, non finibus erat. Praesent accumsan urna vitae pharetra dignissim. Cras luctus risus eros, at lobortis odio lobortis tincidunt. Nulla eget erat porta, semper tellus eget, gravida nisl. Fusce euismod ornare tortor nec posuere. """
)

# LAYING OUT THE FILTERS ROW
st.write("**FILTER BY:**")

row1_1, row1_2, row1_3 = st.columns((1,1,2))

with row1_1:
    id = st.date_input(
    "Desde:",
    #datetime.date(2019, 7, 6)
    value=None, min_value=None, max_value=None)
    
with row1_2:
    fd = st.date_input(
    "Hasta:",
    #datetime.date(2019, 7, 6)
    value=None, min_value=None, max_value=None)

with row1_3:
  department = st.multiselect(
     'Department ',
     ['Amazonas','Antioquia','Arauca','Atlántico','Bolívar','Boyacá','Caldas','Caquetá','Casanare','Cauca','Cesar','Chocó','Córdoba','Cundinamarca','Guainía','Guaviare','Huila','La Guajira','Magdalena','Meta','Nariño','Norte de Santander','Putumayo','Quindío','Risaralda','San Andrés y Providencia','Santander','Sucre','Tolima','Valle del Cauca','Vaupés','Vichada'],
     #['Cesar']
     )
    



# LAYING OUT THE DASHBOARD
row2_1, row2_2 = st.columns(2)

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
col_location= [4.570868,-74.297333]
zoom_level = 5
#midpoint = mpoint(data["lat"], data["lon"])

with row2_1:
    # LAYING OUT THE CHARTS SECTION

    st.write("**Correlation: Vive Digital and Desertion**")
    dftime = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(dftime, x='year', y='lifeExp', color='country', symbol="country")
    st.plotly_chart(fig, use_container_width=True)

    st.write("**Vive Digital by department**")
    dpts=['Amazonas','Antioquia','Arauca','Atlántico','Bolívar','Boyacá','Caldas','Caquetá','Casanare','Cauca','Cesar','Chocó','Córdoba','Cundinamarca','Guainía','Guaviare','Huila','La Guajira','Magdalena','Meta','Nariño','Norte de Santander','Putumayo','Quindío','Risaralda','San Andrés y Providencia','Santander','Sucre','Tolima','Valle del Cauca','Vaupés','Vichada']
    values = ['66','15','117','2','59','86','71','40','96','133','12','70','27','128','67','65','16','7','30','82','28','89','24','92','127','119','96','23','18','65','29','114']
    fig = go.Figure(
    go.Pie(
    labels = dpts,
    values = values,
    hoverinfo = "label+percent",
    textinfo = "value"
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.write("**Desertion history**")
    dftime = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(dftime, x='year', y='lifeExp', color='country', symbol="country")
    st.plotly_chart(fig, use_container_width=True)
    
with row2_2:
    # LAYING OUT THE MAP SECTION
    st.write("**Vive Digital Lotations**")
    DATA_SOURCE = 'https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/fortune_500.csv'
    map(DATA_SOURCE, col_location[0], col_location[1], zoom_level)
