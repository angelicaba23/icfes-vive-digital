import streamlit as st
import pandas as pd
import numpy as np
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

#style
styl = f"""
<style>
  .css-1siy2j7 {{
    width: 10rem;
  }}
  .css-1l269bu{{
    padding: 1rem 0px;
    margin: auto 0 auto auto;
    line-height: 1.2;
  }}
  .h2{{
    padding: 0;
  }}
  .css-ocqkz7{{
    align-items: flex-end;
    justify-content: flex-end;
  }}
  .css-18e3th9 {{
    padding: 1rem 3rem 10rem;
  }}
}}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)


st.title('💾 DATASETS')

#-------------------------------Load Dataframes-------------------------------
df_kioscos = pd.read_csv('assets/Kioscos_Vive_Digital.csv')
df_saber = pd.read_csv('assets/Resultados__nicos_Saber_11_2015-2021.csv')

#-------------------------------1st DataFrame-------------------------------
col1_1, col1_2 = st.columns([10,1])
col1_1.header('1️⃣ Kioscos Vive Digital')
col1_2.download_button(
     label="📥",
     data='assets/Kioscos_Vive_Digital.csv',
     file_name='Kioscos_Vive_Digital.csv',
     mime='text/csv',
 )
pr_kioscos = df_kioscos.profile_report()
with st.expander("ℹ️  Dataframe Profiling"): st_profile_report(pr_kioscos)
st.dataframe(df_kioscos)

#-------------------------------2dn DataFrame-------------------------------
col2_1, col2_2 = st.columns([10,1])
col2_1.header('2️⃣ Saber Pro 11 - ICFES')
col2_2.download_button(
     label="📥",
     data='assets/Resultados__nicos_Saber_11_2015-2021.csv',
     file_name='Resultados__nicos_Saber_11_2015-2021.csv',
     mime='text/csv',
)
pr_saber = df_kioscos.profile_report()
with st.expander("ℹ️ Dataframe Profiling"): st_profile_report(pr_saber)
st.dataframe(df_saber)