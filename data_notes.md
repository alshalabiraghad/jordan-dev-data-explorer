# Data Notes — development_indicators.csv

## Source 1: World Bank World Development Indicators (WDI) API. 
Free access and no API key required.
https://api.worldbank.org/v2/country/{codes}/indicator/{code}?format=json

## Countries covered
Jordan, Egypt, Lebanon, Saudi Arabia

## Years covered
2010 - 2023

## Indicators

### 1. SL.UEM.1524.ZS — Youth unemployment
- Meaning: the percentage of the youth labor force (ages 15–24) who are without work but available for and actively seeking employment.
- Unit: % of total labor force ages 15-24
- Source/methodology note: this is a modeled estimate produced by the ILO (International Labour Organization) and incorporated into the World Bank's WDI, so it's not a number taken directly from one country's household survey. ILO uses statistical modeling to fill gaps so numbers are comparable across countries.
- Limitations: accuracy problems due to the fact that they're modeled ILO estimates instead of raw national survey figure

### 2. IT.NET.USER.ZS — Internet usage
- Meaning: the percentage of a country's total population that used the internet (from any device) in the last 3 months.
- Unit: % of population
- Limitations: the percentage says nothing about connection quality/speed, or how often people use it

### 3. NY.GDP.MKTP.KD.ZG — GDP growth
- Meaning: the annual percentage change in a country's real GDP (Gross Domestic Product, adjusted for inflation) — how much the economy grew or shrank compared to the previous year
- Unit: annual %
- Limitations: it says nothing about how growth is distributed across the population (a growing economy doesn't mean everyone benefits equally)

### 4. SL.TLF.CACT.FE.ZS — Female labor-force participation
- Meaning: the percentage of the female population aged 15+ who are either employed or actively looking for work.
- Unit: % of female population ages 15+
- Limitations: it only counts participation in the measured/formal labor force, so it can undercount informal or unpaid work, which is significant in some economies. It also says nothing about the quality of work.

## Known data quality notes
All four indicators came back complete (0 not available) for these 4 countries across 2010–2023, but this is a property of these specific indicators/countries, not a guarantee that holds for every indicator that will be added later.

Data retrieved: 11-9-2026


## Source 2: Jordan Department of Statistics (PxWeb)

### Table: Poverty Rate by Governorate and year
- Meaning: the percentage of a governorate's population living below the national poverty line.
- Unit: % of governorate population below the poverty line
- Coverage: all 12 governorates + national total, years 1997/2002/2006/2008/2010
- Access method: it required a POST query with a PxWeb-specific JSON body, rather than a simple GET, and the API's internal variable codes were in Arabic even though the display labels are in English
- Known data quality notes:
  - when the json response was first decoded, an error happened duo to invisible BOM in the response body. The fix was to decode the raw response bytes manually using utf-8-sig.
  - the national totals were presented as a 13th governorate, so we had to either Keep it in the DataFrame, but tag it, or split it out entirely. We chose the second option to make it easier to deal with the data, and to avoid the possibility of querying by groupby("governorate") and forgetting to use the filter.
  - the time coverage is very old/sparse


Data retrieved: 13-9-2026


## Source 3: UNDP Human Development Reports (HDI, GII)

- Meaning: Human Development Index blends three things, health, education, and income into one composite score. Gender Inequality Index is about a different three things, reproductive health, empowerment, and labor market participation. 
- Unit: a scale 0-1. for HDI, closer to 1 means higher development (good). for GII, it's the opposite, closer to 0 means more equality (good), and closer to 1 means more inequality (bad).
- Access method: Downloaded a CSV file "All composite indices and components time series (1990–2023)" from the UNDP HDR data center.
- File used: HDR25_Composite_indices_complete_time_series.csv
- Coverage: JOR, EGY, LBN, SAU on years ranged 1990-2023 in the source file but i dropped the years where the value is NA

- Known data quality notes:
  - Encoding: when the file was read first time an error was thrown, UnicodeDecodeError ,meaning this file simply wasn't saved as UTF-8 in the first place, so i explicitly told pandas to use encoding="cp1252".
  - Country name mismatch: in this new data set, Egypt was written as "Egypt" while in the locations table its named as "Egypt, Arab Rep.", so i had to make them match to avoid any errors or unwanted new rows in the database, so i chose to change the name in the new data set, not change the one already used in the database.
  - Missing data: Lebanon has no HDI reported from 1990-2004. For GII, several countries missing in the earliest years, decreasing down to zero by around 2007, meaning GII coverage was extended backward in time for different countries at different points. 
  - Decision on missing values: I dropped them. It's not a situation where I can invent/estimate values.

- Row counts: HDI = 121, GII = 96 (out of 136 possible each, for 4 countries × 34 years)

Data retrieved: 22-9-2026
