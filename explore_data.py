import requests
import pandas as pd

url = "https://api.worldbank.org/v2/country/JOR/indicator/SL.UEM.1524.ZS?format=json&date=2010:2023&per_page=100"

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
    rows.append({"year": entry["date"], "value": entry["value"]})

print(rows)

df = pd.DataFrame(rows)

print(df.info())
print(df.head(10))
print(df["value"].isna().sum())

df["year"] = df["year"].astype(int)

recent = df[df["year"] >= 2020]

print(recent)
print(recent["value"].mean())
print(df.head(10))