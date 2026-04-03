
import requests
import pandas as pd
import os
from supabase import create_client
from datetime import datetime
from bs4 import BeautifulSoup

SUPABASE_URL = os.environ["https://certtklwfzhrazsrqwgp.supabase.co"]
SUPABASE_KEY = os.environ["sb_publishable_LzYPt0XFHN2uYtTk0opacw_0bEPS1U1"]


url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url, timeout=20)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

rows = []

for country in soup.select(".country"):
    name = country.select_one(".country-name").get_text(strip=True)
    capital = country.select_one(".country-capital").get_text(strip=True)
    pop_text = country.select_one(".country-population").get_text(strip=True)
    area_text = country.select_one(".country-area").get_text(strip=True)

    rows.append({
        "Country": name,
        "Capital": capital,
        "Population_Raw": pop_text,
        "Area_Raw": area_text
    })


df = pd.DataFrame(rows)


df["Population"] = (
    df["Population_Raw"]
    .str.replace(r"[^0-9.]", "", regex=True)
    .astype(float)
    .astype(int) 
)

df["Area (sq km)"] = (
    df["Area_Raw"]
    .str.replace(r"[^0-9.]", "", regex=True)
    .astype(float)
)


df = df[["Country", "Capital", "Population", "Area (sq km)"]]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

scrape_time = datetime.now().isoformat()

rows = []

for _, row in df.iterrows():
    rows.append({
        "country_name": str(row.get("Country", "")),
        "capital":      str(row.get("Capital", "")),
        "population":   int(row.get("Population", 0)),
        "area_sq_km":   float(row.get("Area (sq km)", 0.0)),
        "scraped_at":   scrape_time,
    })
