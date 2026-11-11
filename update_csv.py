import requests
import pandas as pd

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

# Aktuelle S&P500 Liste laden
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S%26P_500_component_stocks"

response = requests.get(url, headers=headers)
response.raise_for_status()

sp500_wiki = pd.read_html(response.text)[0]

# Nur benötigte Spalten
sp500 = sp500_wiki[[
    "Symbol",
    "Security",
    "GICS Sector"
]].copy()

# CSV erstellen
sp500.to_csv(
    "constituents_new.csv",
    index=False,
    encoding="utf-8-sig"
)

print("CSV erstellt. Dateinamen oder Verweis in sampling.py entsprechend anpassen")
print(f"Anzahl Unternehmen: {len(sp500)}")