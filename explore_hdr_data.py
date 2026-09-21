import pandas as pd

hdr_df = pd.read_csv("HDR25_Composite_indices_complete_time_series.csv", encoding="cp1252")

hdi_cols = [c for c in hdr_df.columns if c.startswith("hdi_") and "rank" not in c and "_f_" not in c and "_m_" not in c]
gii_cols = [c for c in hdr_df.columns if c.startswith("gii_") and "rank" not in c and "_f_" not in c and "_m_" not in c]

hdr_df = hdr_df[hdr_df["iso3"].isin(["JOR", "EGY", "LBN", "SAU"])]
hdr_df = hdr_df[["country"] + hdi_cols + gii_cols]
hdr_df["country"] = hdr_df["country"].replace("Egypt", "Egypt, Arab Rep.")
hdr_df.rename(columns={"country": "location_name"}, inplace=True)

hdi_long = hdr_df.melt(id_vars=["location_name"], value_vars=hdi_cols, var_name="year_col", value_name="value")
hdi_long["year"] = hdi_long["year_col"].str.replace("hdi_", "").astype(int)
hdi_long["indicator_code"] = "HDI"
hdi_long = hdi_long.drop(columns=["year_col"])

gii_long = hdr_df.melt(id_vars=["location_name"], value_vars=gii_cols, var_name="year_col", value_name="value")
gii_long["year"] = gii_long["year_col"].str.replace("gii_", "").astype(int)
gii_long["indicator_code"] = "GII"
gii_long = gii_long.drop(columns=["year_col"])

hdi_long = hdi_long.dropna(subset=["value"])
gii_long = gii_long.dropna(subset=["value"])

hdr_obs = pd.concat([hdi_long, gii_long], ignore_index=True)
hdr_obs.to_csv("hdr_indicators.csv", index=False)