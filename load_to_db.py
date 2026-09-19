import os
from dotenv import load_dotenv
import psycopg
import pandas as pd

wdi_df = pd.read_csv("development_indicators.csv")
poverty_df = pd.read_csv("poverty_by_governorate.csv")
national_df = pd.read_csv("national_poverty_totals.csv")

load_dotenv()

conn = psycopg.connect(
    dbname="jordan_dev_data",
    user="postgres",
    password=os.environ["DB_PASSWORD"],
    host="localhost",
    port=5432
)

cur = conn.cursor()

indicator_map = {
    "Unemployment, youth total (% of total labor force ages 15-24) (modeled ILO estimate)" : {
        "code": "SL.UEM.1524.ZS",
        "unit": "% of total labor force ages 15-24",
        "source": "World Bank WDI API"
    },
    "Individuals using the Internet (% of population)" : {
        "code": "IT.NET.USER.ZS",
        "unit": "% of population",
        "source": "World Bank WDI API"
    },
    "GDP growth (annual %)" : {
        "code": "NY.GDP.MKTP.KD.ZG",
        "unit": "annual %",
        "source": "World Bank WDI API"
    },
    "Labor force participation rate, female (% of female population ages 15+) (modeled ILO estimate)" : {
        "code": "SL.TLF.CACT.FE.ZS",
        "unit": "% of female population ages 15+",
        "source": "World Bank WDI API"
    },
}

code_lookup = {name: info["code"] for name, info in indicator_map.items()}
wdi_df["indicator_code"] = wdi_df["indicator"].map(code_lookup)

poverty_df["indicator_code"] = "DOS_POVERTY_RATE_GOV"
national_df["indicator_code"] = "DOS_POVERTY_RATE_GOV"

indicators_to_insert = [
    (info["code"], name, info["unit"], info["source"])
    for name, info in indicator_map.items()
]
indicators_to_insert.append((
    "DOS_POVERTY_RATE_GOV",
    "Poverty rate",
    "% of governorate population below poverty line",
    "Jordan DOS PxWeb API"
))

cur.executemany("INSERT INTO indicators (indicator_code, indicator_name, unit, source) VALUES (%s, %s, %s, %s) ON CONFLICT (indicator_code) DO NOTHING", indicators_to_insert)
conn.commit()

national_df["governorate"] = "Jordan"

countries = wdi_df["country"].unique()
governorates = poverty_df["governorate"].unique()

locations_to_insert = (
    [(c, "country") for c in countries]
    + [(g, "governorate") for g in governorates]
)

cur.executemany("INSERT INTO locations (location_name, location_type) VALUES (%s, %s) ON CONFLICT (location_name) DO NOTHING", locations_to_insert)
conn.commit()

wdi_obs = list(wdi_df[["indicator_code", "country", "year", "value"]].itertuples(index=False, name=None))
poverty_obs = list(poverty_df[["indicator_code", "governorate", "year", "poverty_rate"]].itertuples(index=False, name=None))
national_obs = list(national_df[["indicator_code", "governorate", "year", "poverty_rate"]].itertuples(index=False, name=None))

all_observations = wdi_obs + poverty_obs + national_obs

cur.executemany("INSERT INTO observations (indicator_code, location_name, year, value) VALUES (%s, %s, %s, %s) ON CONFLICT (indicator_code, location_name, year) DO NOTHING", all_observations)
conn.commit()

cur.close()
conn.close() 

