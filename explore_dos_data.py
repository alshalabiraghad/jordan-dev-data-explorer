import pandas as pd
import requests
import json

metadata_url = "https://jorinfo.dos.gov.jo/Databank/api/v1/en/Poverty/Poverty-Indicators/Table1.px"

response = requests.get(metadata_url)

print(response.json())

metadata = response.json()

query = {
    "query": [
        {
            "code": metadata["variables"][0]["code"],
            "selection": {
                "filter": "item",
                "values": metadata["variables"][0]["values"]
            }
        },
        {
            "code": metadata["variables"][1]["code"],
            "selection": {
                "filter": "item",
                "values": metadata["variables"][1]["values"]
            }
        }
    ],
    "response": {
        "format": "json"
    }
}

data_response = requests.post(metadata_url, json=query)

raw_text = data_response.content.decode("utf-8-sig")
data = json.loads(raw_text)

print(data)

gov_labels = dict(zip(metadata["variables"][0]["values"], metadata["variables"][0]["valueTexts"]))
year_labels = dict(zip(metadata["variables"][1]["values"], metadata["variables"][1]["valueTexts"]))

rows = []
for entry in data["data"]:
    gov_code, year_code = entry["key"]
    rows.append({
        "governorate": gov_labels[gov_code],
        "year": int(year_labels[year_code]),
        "poverty_rate": float(entry["values"][0])
    })

df_poverty = pd.DataFrame(rows)

national_totals = df_poverty[df_poverty["governorate"] == "Kingdom"].reset_index(drop=True)
df_poverty = df_poverty[df_poverty["governorate"] != "Kingdom"].reset_index(drop=True)

print(national_totals.info())
print(national_totals.head())
print(df_poverty.info())
print(df_poverty.head(15))

national_totals.to_csv("national_poverty_totals.csv", index=False)
df_poverty.to_csv("poverty_by_governorate.csv", index=False)

