Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@angelicaba23 
angelicaba23
/
icfes-vive-digital
Public
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
icfes-vive-digital
/
pages
/
1_📊_Dashboard.py
in
main
 

Spaces

2

No wrap
1
import time
2
import pandas as pd
3
import streamlit as st
4
import plotly.express as px
5
from plotly.subplots import make_subplots
6
import plotly.graph_objects as go
7
​
8
from helper_meth import get_plot
9
#st.set_page_config(layout="wide")
10
#style
11
styl = f"""
12
<style>
13
  .css-1siy2j7 {{
14
    width: 13rem;
15
  }}
16
  .css-18e3th9 {{
17
    padding: 1rem 3rem 10rem;
18
  }}  
19
  .st-ik {{
20
    flex-direction: row;
21
  }}  
22
  
23
</style>
24
"""
25
st.markdown(styl, unsafe_allow_html=True)
26
​
27
st.title('📊 PUNTOS VIVE DIGITAL(PVD) - PRUEBAS SABER 11')
28
​
29
#-------------------------------Show metrics-------------------------------
30
col1_1, col1_2, col1_3, col1_4, col1_5 = st.columns(5)
31
#st.metric(label, value, delta=None, delta_color="normal/off/inverse")
32
col1_1.metric("Score Saber 11 COL", "100", "10")
33
col1_2.metric("Score Saber 11 BAQ", "200", "-4")
34
col1_4.metric("# of PVD", "100", "8%")
35
col1_5.metric("Bandwidth", "100 Hz", "8%")
36
​
37
#-------------------------------Load Dataframes-------------------------------
38
df_kioscos = pd.read_csv('assets/Kioscos_Vive_Digital.csv')
39
df_kioscos['PERIODO'] = df_kioscos['FECHA INAUGURACION'].astype(str).str.split('-', expand=True)[0]
40
df_kioscos['PERIODO'] = df_kioscos['PERIODO'].replace(['1900'],['2019'])
41
​
42
df_saber = pd.read_csv('assets/Resultados__nicos_Saber_11_2015-2021.csv')
43
df_saber['PERIODO'] = df_saber['PERIODO'].replace([20151,20161,20171,20181,20191,20201,20211],['2015','2016','2017','2018','2019','2020','2021'])
44
​
45
#-------------------------------Sidebar-------------------------------
46
st.sidebar.write('### Filter:')
47
​
48
years = ['2015','2016','2017','2018','2019','2020','2021']
49
selected_years = st.sidebar.select_slider('Select the year range:', years, value=[min(years),max(years)])
50
​
51
types = ["Mean","Median","Maximum","Minimum"]
52
selected_measure_type = st.sidebar.selectbox ("Select the measure type:", types, key = 'measure_type')
53
​
54
#departments = ['Amazonas','Antioquia','Arauca','Atlántico','Bolívar','Boyacá','Caldas','Caquetá','Casanare','Cauca','Cesar','Chocó','Córdoba','Cundinamarca','Guainía','Guaviare','Huila','La Guajira','Magdalena','Meta','Nariño','Norte de Santander','Putumayo','Quindío','Risaralda','San Andrés y Providencia','Santander','Sucre','Tolima','Valle del Cauca','Vaupés','Vichada'],
55
     
56
selected_department = st.sidebar.multiselect(
57
    'Select the Departments',
58
    list(df_kioscos.DEPARTAMENTO.unique()),
59
    ['ANTIOQUIA'])
60
    
61
#st.write([dpto for dpto in list(df_kioscos.DEPARTAMENTO.unique()) if dpto not in selected_department])
62
​
63
#-------------------------------Filterd DF-------------------------------
64
df_kioscos_filtered = df_kioscos[(df_kioscos.PERIODO.astype(int) >= int(selected_years[0])) & (df_kioscos.PERIODO.astype(int) <= int(selected_years[1]))]
65
df_kioscos_filtered = df_kioscos_filtered[(df_kioscos_filtered['DEPARTAMENTO'].isin(selected_department))]
66
​
67
#df_saber_filtered = df_saber[(df_saber['PERIODO'] == '2015') | (df_saber['PERIODO'] == '2016') | (df_saber['PERIODO'] == '2017') | (df_saber['PERIODO'] == '2018') | (df_saber['PERIODO'] == '2019') | (df_saber['PERIODO'] == '2020') | (df_saber['PERIODO'] == '2021')]
68
df_saber_filtered = df_saber[(df_saber.PERIODO.astype(int) >= int(selected_years[0])) & (df_saber.PERIODO.astype(int) <= int(selected_years[1]))]
69
df_saber_filtered = df_saber_filtered[(df_saber_filtered['COLE_DEPTO_UBICACION'].isin(selected_department))]
70
​
71
df4 = df_kioscos_filtered.groupby(by=['MUNICIPIO', 'PERIODO']).count().reset_index()
72
​
73
if selected_measure_type == "Mean":
74
  df1 = df_saber_filtered.groupby(by=['COLE_MCPIO_UBICACION', 'PERIODO']).mean().reset_index().sort_values()
@angelicaba23
Commit changes
Commit summary
Create 1_📊_Dashboard.py
Optional extended description
Add an optional extended description…
 Commit directly to the main branch.
 Create a new branch for this commit and start a pull request. Learn more about pull requests.
 
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
You have no unread notifications
