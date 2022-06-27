import numpy as np
import plotly.express as px
import streamlit as st

def get_years(df_data):
    """
    Returns the years in the dataframe SABER 11
    """
    return np.unique(df_data.PERIODO).tolist()

#@streamlit.cache
def get_plot(df, year, teams_colorscale):
    data = df.dropna().reset_index()
    data = data.astype(
        dtype={"PERIODO": "int32"}
    )
    year = 20194
    data = data.loc[data.reset_index()["year"] == 20194]
    return px.scatter(
        data,
        x="COLE_MCPIO_UBICACION",
        y="PUNT_GLOBAL",
        labels={
            "COLE_MCPIO_UBICACION": "Roster Turnover (Difference in minutes played by player -- see below)",
            "PUNT_GLOBAL": "Regular Season Wins",
        },
        color="COLE_COD_DEPTO_UBICACION",
        color_discrete_sequence=teams_colorscale,
    )

