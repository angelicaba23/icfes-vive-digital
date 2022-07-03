import time
import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests

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
  .st-ea {{
    flex-direction: row;
  }}  
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

st.title('📊 PUNTOS VIVE DIGITAL(PVD) - PRUEBAS SABER 11')

#-------------------------------Layout Metrics-------------------------------
col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns(5)
#st.metric(label, value, delta=None, delta_color="normal/off/inverse")

#-------------------------------Load Dataframes-------------------------------
df_kioscos = pd.read_csv('assets/Kioscos_Vive_Digital.csv', parse_dates=['FECHA INAUGURACION'],decimal=",")
df_kioscos['AÑO'] = df_kioscos['FECHA INAUGURACION'].dt.year
df_kioscos['PERIODO'] = df_kioscos['FECHA INAUGURACION'].astype(str).str.split('-', expand=True)[0]
df_kioscos['PERIODO'] = df_kioscos['PERIODO'].replace(['1900'],['2019'])

df_saber = pd.read_csv('assets/Resultados__nicos_Saber_11_2014-2021.csv')
df_saber['PERIODO'] = df_saber['PERIODO'].replace([20141,20151,20161,20171,20181,20191,20201,20211],['2014','2015','2016','2017','2018','2019','2020','2021'])

res = requests.get("https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json")
#res = 'assets/Colombia.geo.json'
#-------------------------------Sidebar-------------------------------
st.sidebar.write('### Filter:')

years = ['2015','2016','2017','2018','2019','2020','2021']
selected_years = st.sidebar.select_slider('Select the year range:', years, value=[min(years),max(years)])
syear = [selected_years[0]]
for i in range(int(selected_years[1])-int(selected_years[0])):
  syear.append(int(selected_years[0])+i+1)

types = ["Mean","Median","Maximum","Minimum"]
selected_measure_type = st.sidebar.selectbox ("Select the measure type:", types, key = 'measure_type')

#departments = ['Amazonas','Antioquia','Arauca','Atlántico','Bolívar','Boyacá','Caldas','Caquetá','Casanare','Cauca','Cesar','Chocó','Córdoba','Cundinamarca','Guainía','Guaviare','Huila','La Guajira','Magdalena','Meta','Nariño','Norte de Santander','Putumayo','Quindío','Risaralda','San Andrés y Providencia','Santander','Sucre','Tolima','Valle del Cauca','Vaupés','Vichada'],
     
selected_department = st.sidebar.multiselect(
    'Select the Departments',
    list(df_kioscos.DEPARTAMENTO.unique()),
    ['ANTIOQUIA'])

st.write(len(selected_department))
    
#st.write([dpto for dpto in list(df_kioscos.DEPARTAMENTO.unique()) if dpto not in selected_department])

#-------------------------------Filterd DF-------------------------------
if len(selected_department) != 0:
  df_kioscos_filtered = df_kioscos[(df_kioscos.PERIODO.astype(int) <= int(selected_years[0])) & (df_kioscos.PERIODO.astype(int) <= int(selected_years[1]))]
  df_kioscos_filtered = df_kioscos_filtered[(df_kioscos_filtered['DEPARTAMENTO'].isin(selected_department))]
  
  df_mapplot_mun = df_kioscos[(df_kioscos.PERIODO.astype(int) <= int(selected_years[1]))]
  df_mapplot_mun = df_kioscos_filtered[(df_kioscos_filtered['DEPARTAMENTO'].isin(selected_department))]
  
  #df_saber_filtered = df_saber[(df_saber['PERIODO'] == '2015') | (df_saber['PERIODO'] == '2016') | (df_saber['PERIODO'] == '2017') | (df_saber['PERIODO'] == '2018') | (df_saber['PERIODO'] == '2019') | (df_saber['PERIODO'] == '2020') | (df_saber['PERIODO'] == '2021')]
  df_saber_filtered = df_saber[(df_saber.PERIODO.astype(int) >= int(selected_years[0])) & (df_saber.PERIODO.astype(int) <= int(selected_years[1]))]
  df_saber_filtered = df_saber_filtered[(df_saber_filtered['COLE_DEPTO_UBICACION'].isin(selected_department))]

else:
  df_kioscos_filtered = df_kioscos[(df_kioscos.PERIODO.astype(int) <= int(selected_years[0])) & (df_kioscos.PERIODO.astype(int) <= int(selected_years[1]))]
  df_saber_filtered = df_saber[(df_saber.PERIODO.astype(int) >= int(selected_years[0])) & (df_saber.PERIODO.astype(int) <= int(selected_years[1]))]
  df_mapplot_mun = df_kioscos[(df_kioscos.PERIODO.astype(int) <= int(selected_years[1]))]
  
df4 = df_kioscos_filtered.groupby(by=['MUNICIPIO', 'PERIODO']).count().reset_index()
df_mapplot_mun = df_mapplot_mun.groupby('MUNICIPIO').agg({'COORDENADAS DE REFERENCIA LATITUD': 'first', 'COORDENADAS DE REFERENCIA LONGITUD': 'first', 'CODIGO DIRCON':'count'}).reset_index()
df_mapplot_mun.rename(columns = {'CODIGO DIRCON':'Count_PVD'},inplace = True) #Count_PVD = Count Puntos Vive Digital

if selected_measure_type == "Mean":
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).mean().reset_index()
  
if selected_measure_type == "Median":
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).median().reset_index()

if selected_measure_type == "Maximum":
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).max().reset_index()

if selected_measure_type == "Minimum":
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).min().reset_index()

#-------------------------------Layout Metrics-------------------------------
col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns(5)
#st.metric(label, value, delta=None, delta_color="normal/off/inverse")

col1_1.metric("Score Saber 11 COL 2014-2016", str(round(df_saber.PUNT_GLOBAL.mean(),5)))
col1_2.metric("Score Saber 11", str(round(df_saber_filtered.PUNT_GLOBAL.mean(),5)))
col1_4.metric("# of PVD", str(len(df_kioscos_filtered)))
col1_5.metric("Bandwidth", str(round(df_kioscos_filtered['VELOCIDADSUBIDA (Kb)'].mean(),2)) + ' Hz')

#-------------------------------Graphs-------------------------------
#Graphs Layout
col2_1, col2_2 = st.columns(2)
col3_1, col3_2 = st.columns(2)

#Graphs Title
col2_1.write('### Graph Score Saber 11')
col2_2.write('### Map PVD')
col3_1.write('### Graph Score Saber 11 by subjet')
col3_2.write('### Graph # of PVD installed')
#st.write('### CORRELATION')

#Graphs Description
col2_1.markdown(' Graph Score Saber 11')
col2_2.markdown(' Map PVD')
col3_1.markdown(' Graph Score Saber 11 by subjet')
col3_2.markdown(' Graph # of PVD installed by year')
#st.markdown(' Corr')

#Graph Score Saber 11
fig1 = px.line(
        df1.sort_values(by='PERIODO', ascending=True),
        x="PERIODO",
        y="PUNT_GLOBAL",
        labels={
            "PERIODO": "Years",
            "PUNT_GLOBAL": "Overall Score Saber Pro",
            "COLE_MCPIO_UBICACION":"Boroughs",
        },
        color="COLE_MCPIO_UBICACION",
        markers=True,
)
col2_1.plotly_chart(fig1, use_container_width=True)

#Graph Map PVD
fig2 = px.scatter_mapbox(df_mapplot_mun, lat="COORDENADAS DE REFERENCIA LATITUD", lon="COORDENADAS DE REFERENCIA LONGITUD", size = df_mapplot_mun["Count_PVD"]
                        ,  hover_name="MUNICIPIO", hover_data=["MUNICIPIO", "Count_PVD"], color="Count_PVD"
                        ,color_continuous_scale=px.colors.sequential.Rainbow).update_layout(
    mapbox={
        "style": "carto-positron",
        "zoom": 5.1,
        "layers": [
            {
                "source": res.json(),
                #"source": res,
                "type": "line",
                "color": "gray",
                "line": {"width": 1},
            }
        ],
    }
)
col2_2.plotly_chart(fig2, use_container_width=True)

#Graph Score Saber 11 by subjet
sbj = {'ENGLISH':'PUNT_INGLES','MATH':'PUNT_MATEMATICAS','SOCIAL SCIENCES':'PUNT_SOCIALES_CIUDADANAS','NATURAL SCIENCES':'PUNT_C_NATURALES','CRITICAL READING':'PUNT_LECTURA_CRITICA'}
yline = col3_1.radio('',tuple(sbj.keys()),)

fig3 = px.line(
        df1.sort_values(by='PERIODO', ascending=True),
        x="PERIODO",
        y=sbj[yline],
        labels={
            "PERIODO": "Years",
            "PUNT_GLOBAL": "Score Saber Pro",
            "COLE_MCPIO_UBICACION":"Boroughs",
        },
        color="COLE_MCPIO_UBICACION",
        markers=True,
)
col3_1.plotly_chart(fig3, use_container_width=True)

#Graph # of PVD
if len(selected_years) > 1: ypie = col3_2.radio('',tuple(syear))
df4 = df4[(df4.PERIODO.astype(int) == int(ypie))].reset_index(drop=True)

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
else: col3_2.warning(f'There are no PVD installed in {ypie}')

