# Data Notes — development_indicators.csv

## Source
World Bank World Development Indicators (WDI) API. 
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

Data retrieved: 12-9-2026