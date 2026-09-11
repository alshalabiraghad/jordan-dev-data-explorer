import requests
import pandas as pd

def fetch_indicator(indicator_code, countries, start_date, end_date):
    country_str = ";".join(countries)

    url = f"https://api.worldbank.org/v2/country/{country_str}/indicator/{indicator_code}?format=json&date={start_date}:{end_date}&per_page=100"
    response = requests.get(url)

    data = response.json()

    records = data[1]

    rows = []
    for entry in records:
        rows.append({"indicator" : entry["indicator"]["value"],
                    "country" : entry["country"]["value"],
                    "year": entry["date"],
                    "value": entry["value"]})

    df = pd.DataFrame(rows)

    df["year"] = df["year"].astype(int) 

    return df

unemployment = fetch_indicator("SL.UEM.1524.ZS", ["JOR", "EGY", "LBN", "SAU"], 2010, 2023)
internet = fetch_indicator("IT.NET.USER.ZS", ["JOR", "EGY", "LBN", "SAU"], 2010, 2023)
gdp_growth = fetch_indicator("NY.GDP.MKTP.KD.ZG", ["JOR", "EGY", "LBN", "SAU"], 2010, 2023)
female_lfp = fetch_indicator("SL.TLF.CACT.FE.ZS", ["JOR", "EGY", "LBN", "SAU"], 2010, 2023)

print(unemployment.info())
print(unemployment["value"].isna().sum())
print(internet.info())
print(internet["value"].isna().sum())
print(gdp_growth.info())
print(gdp_growth["value"].isna().sum())
print(female_lfp.info())
print(female_lfp["value"].isna().sum())

combined = pd.concat([unemployment, internet, gdp_growth, female_lfp], ignore_index=True)
combined.to_csv("development_indicators.csv", index=False)

print(combined.shape)
print(combined["indicator"].unique())
print(combined.isna().sum())

recent = combined[combined["year"] >= 2020]

print(recent)
print(recent["value"].mean())

country_avg = combined.groupby("country")["value"].mean()

print(country_avg)