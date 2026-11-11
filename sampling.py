import pandas as pd
import numpy as np
import yfinance as yf

START = "2018-01-01"
END   = "2026-01-01"

sp500_const = pd.read_csv("constituents.csv")

# Relevante Sektoren auswählen
SECTORS_KEEP = {
    "Information Technology": "Technology",
    "Financials":              "Financials",
    "Health Care":             "Healthcare",
    "Energy":                  "Energy",
    "Consumer Staples":        "Consumer",
    "Consumer Discretionary":  "Consumer",
}

# Ticker bereinigen
sp500_const = sp500_const[sp500_const["GICS Sector"].isin(SECTORS_KEEP)].copy()
sp500_const["Sector_clean"] = sp500_const["GICS Sector"].map(SECTORS_KEEP)
sp500_const["Symbol"] = sp500_const["Symbol"].str.replace(".", "-", regex=False)

universe = sp500_const[["Symbol", "Sector_clean"]].rename(
    columns={"Symbol": "Ticker", "Sector_clean": "Sektor"}
).reset_index(drop=True)

print(f"Universum: {len(universe)} Aktien")
print(universe["Sektor"].value_counts().to_dict())


all_candidates = universe["Ticker"].tolist()

# Download über yfinance
raw_candidate_prices = yf.download(
    all_candidates + ["^GSPC", "^VIX"],
    start=START,
    end=END,
    auto_adjust=True,
    progress=False
)["Close"]

# Survivorship Kriterium
# Aktie berücksichtigt, wenn an START und END gelistet
trading_days = raw_candidate_prices["^VIX"].dropna().index

first_trading_day = trading_days[0]
last_trading_day  = trading_days[-1]

print(f"\nErster Handelstag: {first_trading_day.date()}")
print(f"Letzter Handelstag: {last_trading_day.date()}")

has_start_price = raw_candidate_prices.loc[first_trading_day, all_candidates].notna()
has_end_price   = raw_candidate_prices.loc[last_trading_day, all_candidates].notna()

survivors = [
    ticker
    for ticker in all_candidates
    if has_start_price[ticker] and has_end_price[ticker]
]

# Sektor-Mapping für Überlebende
survivor_map = universe.set_index("Ticker")["Sektor"].to_dict()
survivor_map = {
    t: s for t, s in survivor_map.items()
    if t in survivors
}

# Pool je Sektor
pool_by_sector = {}
for sector in SECTORS_KEEP.values():
    pool_by_sector[sector] = [
        t for t, s in survivor_map.items()
        if s == sector
    ]

print(
    f"\nSurvivors: {len(survivors)} Aktien "
    f"(Kurs am {first_trading_day.date()} und "
    f"{last_trading_day.date()} vorhanden)"
)
print({sec: len(pool) for sec, pool in pool_by_sector.items()})


# Stichprobenziehung
N_PER_STRATUM = 6
RANDOM_STATE  = 42

sampled = {}
for sector, pool in pool_by_sector.items():
    if len(pool) < N_PER_STRATUM:
        raise ValueError(f"Zu wenige Überlebende in Sektor {sector}: {len(pool)}")
    sampled[sector] = (
        pd.Series(pool)
        .sample(n=N_PER_STRATUM, random_state=RANDOM_STATE)
        .tolist()
    )

all_tickers = [t for tlist in sampled.values() for t in tlist]
sector_map  = {t: s for s, tlist in sampled.items() for t in tlist}

# Preisreihen extrahieren
raw_prices = raw_candidate_prices[all_tickers + ["^VIX"]].copy()

print(f"\nraw_prices: {raw_prices.shape[0]} Tage × {raw_prices.shape[1]} Spalten")
print(f"Enthält: {len(all_tickers)} Aktien + VIX")