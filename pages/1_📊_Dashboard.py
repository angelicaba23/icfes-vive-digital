import time
import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helper_meth import get_plot
#st.set_page_config(layout="wide")
#style
styl = f"""
<style>
  .css-1siy2j7 {{
    width: 13rem;
  }}
  .css-18e3th9 {{
    padding: 1rem 3rem 10rem;
  }}  
  .st-ik {{
    flex-direction: row;
  }}  
  
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

st.title('📊 PUNTOS VIVE DIGITAL(PVD) - PRUEBAS SABER 11')

#-------------------------------Show metrics-------------------------------
col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns(5)
#st.metric(label, value, delta=None, delta_color="normal/off/inverse")
col1_1.metric("Score Saber 11 COL", "100", "10")
col1_2.metric("Score Saber 11 BAQ", "200", "-4")
col1_4.metric("# of PVD", "100", "8%")
col1_5.metric("Bandwidth", "100 Hz", "8%")

#-------------------------------Load Dataframes-------------------------------
df_kioscos = pd.read_csv('assets/Kioscos_Vive_Digital.csv')
df_kioscos['PERIODO'] = df_kioscos['FECHA INAUGURACION'].astype(str).str.split('-', expand=True)[0]
df_kioscos['PERIODO'] = df_kioscos['PERIODO'].replace(['1900'],['2019'])

df_saber = pd.read_csv('assets/Resultados__nicos_Saber_11_2015-2021.csv')
df_saber['PERIODO'] = df_saber['PERIODO'].replace([20151,20161,20171,20181,20191,20201,20211],['2015','2016','2017','2018','2019','2020','2021'])

#-------------------------------Sidebar-------------------------------
st.sidebar.write('### Filter:')

years = ['2015','2016','2017','2018','2019','2020','2021']
selected_years = st.sidebar.select_slider('Select the year range:', years, value=[min(years),max(years)])

types = ["Mean","Median","Maximum","Minimum"]
selected_measure_type = st.sidebar.selectbox ("Select the measure type:", types, key = 'measure_type')

#departments = ['Amazonas','Antioquia','Arauca','Atlántico','Bolívar','Boyacá','Caldas','Caquetá','Casanare','Cauca','Cesar','Chocó','Córdoba','Cundinamarca','Guainía','Guaviare','Huila','La Guajira','Magdalena','Meta','Nariño','Norte de Santander','Putumayo','Quindío','Risaralda','San Andrés y Providencia','Santander','Sucre','Tolima','Valle del Cauca','Vaupés','Vichada'],
     
selected_department = st.sidebar.multiselect(
    'Select the Departments',
    list(df_kioscos.DEPARTAMENTO.unique()),
    ['ANTIOQUIA'])
    
#st.write([dpto for dpto in list(df_kioscos.DEPARTAMENTO.unique()) if dpto not in selected_department])

#-------------------------------Filterd DF-------------------------------
df_kioscos_filtered = df_kioscos[(df_kioscos.PERIODO.astype(int) >= int(selected_years[0])) & (df_kioscos.PERIODO.astype(int) <= int(selected_years[1]))]
df_kioscos_filtered = df_kioscos_filtered[(df_kioscos_filtered['DEPARTAMENTO'].isin(selected_department))]

#df_saber_filtered = df_saber[(df_saber['PERIODO'] == '2015') | (df_saber['PERIODO'] == '2016') | (df_saber['PERIODO'] == '2017') | (df_saber['PERIODO'] == '2018') | (df_saber['PERIODO'] == '2019') | (df_saber['PERIODO'] == '2020') | (df_saber['PERIODO'] == '2021')]
df_saber_filtered = df_saber[(df_saber.PERIODO.astype(int) >= int(selected_years[0])) & (df_saber.PERIODO.astype(int) <= int(selected_years[1]))]
df_saber_filtered = df_saber_filtered[(df_saber_filtered['COLE_DEPTO_UBICACION'].isin(selected_department))]

df4 = df_kioscos_filtered.groupby(by=['MUNICIPIO', 'PERIODO']).count().reset_index()

if selected_measure_type == "Mean":
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).mean().reset_index().sort_values()
  
if selected_measure_type == "Median":
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).median().reset_index()

if selected_measure_type == "Maximum":
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).max().reset_index()

if selected_measure_type == "Minimum":
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).min().reset_index()

#df4 = df_kioscos_filtered.groupby('DEPARTAMENTO')['CODIGO DIRCON'].count().sort_values(ascending=False)

#-------------------------------Graphs-------------------------------
#Graphs Layout
col2_1, col2_2 = st.columns(2)
col3_1, col3_2 = st.columns(2)

#Graphs Title
col2_1.write('### Graph Score Saber 11')
col2_2.write('### Map PVD')
col3_1.write('### Graph Score Saber 11 by subjet')
col3_2.write('### Graph # of PVD')
st.write('### CORRELATION')

#Graphs Description
col2_1.markdown(' Graph Score Saber 11')
col2_2.markdown(' Map PVD')
col3_1.markdown(' Graph Score Saber 11 by subjet')
col3_2.markdown(' Graph # of PVD installed by year')
st.markdown(' Corr')

#Graph Score Saber 11
fig1 = px.line(
        df1,
        x="PERIODO",
        y="PUNT_GLOBAL",
        labels={
            "PERIODO": "Years",
            "PUNT_GLOBAL": "Score Saber Pro",
            "COLE_MCPIO_UBICACION":"Boroughs",
        },
        color="COLE_MCPIO_UBICACION",
        markers=True,
)
col2_1.plotly_chart(fig1, use_container_width=True)

#Graph Map PVD
#Graph Score Saber 11 by subjet

#Graph # of PVD
if len(selected_years) > 1:
  ypie = col3_2.radio('',tuple(df_kioscos.PERIODO.sort_values().unique()))

df4 = df4[(df4.PERIODO.astype(int) == int(ypie))].reset_index(drop=True)
col3_1.write(df4.size)
col3_1.write(df4)

if df4.size != 0:
  fig4 = px.pie(df4,
                values='OPERADOR',
                names='MUNICIPIO',
                #title='',
                #hover_data=['lifeExp']
                labels={'OPERADOR':'# of PVD',
                        'MUNICIPIO':'Boroughs',
                })
  fig4.update_traces(textposition='inside', textinfo='percent+label')
  col3_2.plotly_chart(fig4, use_container_width=True)
else:
  col3_2.warning(f'There are no PVD in {ypie}')
