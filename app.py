import streamlit as st
import pandas as pd 
import psycopg2
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

st.title("Jordan Development Data Explorer")

load_dotenv()

@st.cache_resource
def get_connection():
    return psycopg2.connect(dbname="jordan_dev_data", user="postgres", password=os.getenv("DB_PASSWORD"), host="localhost")

@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

conn = get_connection()
client = get_client()

df = pd.read_sql("SELECT o.indicator_code, i.indicator_name, o.location_name, o.year, o.value FROM observations o " \
"JOIN indicators i ON o.indicator_code = i.indicator_code", conn)

list_of_indicators = df["indicator_name"].unique().tolist()
selected_indicator = st.selectbox("Choose an indicator", list_of_indicators)

df_filtered = df[df["indicator_name"] == selected_indicator]

list_of_locations = df_filtered["location_name"].unique().tolist()
selected_locations = st.multiselect("Choose location/s", list_of_locations, default=list_of_locations)

min_year = int(df_filtered["year"].min())
max_year = int(df_filtered["year"].max())
selected_year_range = st.slider("Choose year range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

df_filtered = df_filtered[df_filtered["location_name"].isin(selected_locations)]
df_filtered = df_filtered[(df_filtered["year"] >= selected_year_range[0]) & (df_filtered["year"] <= selected_year_range[1])]

df_filtered = df_filtered.pivot(index="year", columns="location_name", values="value")

with st.expander("Sources and Methodology"):
    st.markdown(""" 
    Source 1: World Bank World Development Indicators (WDI) API.
    - Coverage: Jordan, Egypt, Lebanon, Saudi Arabia. Years covered: 2010 - 2023

        1. SL.UEM.1524.ZS — Youth unemployment: The percentage of the youth labor force (ages 15–24) who are without work but available for and actively seeking employment.
            - Unit: % of total labor force ages 15-24
            - Limitations: accuracy problems due to the fact that they're modeled ILO estimates instead of raw national survey figure

        2. IT.NET.USER.ZS — Internet usage: The percentage of a country's total population that used the internet (from any device) in the last 3 months.
            - Unit: % of population
            - Limitations: the percentage says nothing about connection quality/speed, or how often people use it

        3. NY.GDP.MKTP.KD.ZG — GDP growth: The annual percentage change in a country's real GDP (Gross Domestic Product, adjusted for inflation) — how much the economy grew or shrank compared to the previous year
            - Unit: annual %
            - Limitations: it says nothing about how growth is distributed across the population (a growing economy doesn't mean everyone benefits equally)

        4. SL.TLF.CACT.FE.ZS — Female labor-force participation: The percentage of the female population aged 15+ who are either employed or actively looking for work.
            - Unit: % of female population ages 15+
            - Limitations: it only counts participation in the measured/formal labor force, so it can undercount informal or unpaid work, which is significant in some economies. It also says nothing about the quality of work.

    Source 2: Jordan Department of Statistics (PxWeb): the percentage of a governorate's population living below the national poverty line.
    - Unit: % of governorate population below the poverty line
    - Coverage: all 12 governorates + national total, years 1997/2002/2006/2008/2010
    - Known data quality notes:
        - the national totals were presented as a 13th governorate, so we split it out entirely to make it easier to deal with the data.
        - The time coverage is very old/sparse
    
    Source 3: UNDP Human Development Reports (HDI, GII): Human Development Index blends three things, health, education, and income into one composite score. Gender Inequality Index is about a different three things, reproductive health, empowerment, and labor market participation. 
    - Unit: a scale 0-1. for HDI, closer to 1 means higher development (good). for GII, it's the opposite, closer to 0 means more equality (good), and closer to 1 means more inequality (bad).
    - File used: HDR25_Composite_indices_complete_time_series.csv
    - Coverage: JOR, EGY, LBN, SAU on years ranged 1990-2023.
    - Limitations: coverage is uneven, especially for GII (phased in gradually, so earlier years have more missing countries) and HDI for Lebanon (missing 1990-2004). A few isolated large jumps (e.g. Egypt's GII in 2016, Saudi Arabia's in 2013) are more likely UNDP methodology/calculation updates than real one-year social change.
    """)

cols = st.columns(len(selected_locations))
for location, col in zip(selected_locations, cols):
    latest_value = df_filtered.loc[df_filtered[location].last_valid_index(), location]
    first_value = df_filtered.loc[df_filtered[location].first_valid_index(), location]
    col.metric(label=location, value=latest_value, delta= f"{latest_value - first_value:.3f}")

st.line_chart(df_filtered)    
st.dataframe(df_filtered)

st.text_input("Ask a question about the data", key="question_input", placeholder="e.g. What is the trend of youth unemployment in Jordan over the last decade?")
if st.button("Ask"):
    question = st.session_state.question_input
    if not question.strip():
        st.warning("Please enter a question before clicking 'Ask'.")
    else:
        response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction="you are part of a development-data explorer project. Be concise, and be upfront that you don’t yet have access to the project’s actual dataset.",
            temperature=0.3
            )
        )
        st.write(response.text)