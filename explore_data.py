import requests
import pandas as pd

#url = "https://api.worldbank.org/v2/country/JOR/indicator/SL.UEM.1524.ZS?format=json&date=2010:2023&per_page=100"
url = "https://api.worldbank.org/v2/country/JOR;EGY;LBN;SAU/indicator/SL.UEM.1524.ZS?format=json&date=2010:2023&per_page=100"

response = requests.get(url)

print(response.status_code)

data = response.json()

print(type(data))
print(len(data))

#print(data[0])
#print(data[1][0])
#print(data[1][0]['indicator'])
#print("---------------")

records = data[1]

rows = []
for entry in records:
    rows.append({"country" : entry["country"]["value"],
                 "year": entry["date"],
                 "value": entry["value"]})

print(rows)
print("-------------------------")

df = pd.DataFrame(rows)

print(df.info())
print(df.head(10))
print(df["value"].isna().sum())

df["year"] = df["year"].astype(int)

recent = df[df["year"] >= 2020]

print(recent)
print(recent["value"].mean())

df.to_csv("data.csv", index=False)

country_avg = df.groupby("country")["value"].mean()

print(country_avg)
