import pandas as pd

REQUIRED = ["terrestrial_date", "min_temp", "max_temp", "pressure"]

def load_data(path="data/mars_weather.csv"):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()

    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}. "
                         f"Colonnes disponibles : {list(df.columns)}")

    df = df.drop(columns=["index", "id"], errors="ignore")

    df["terrestrial_date"] = pd.to_datetime(df["terrestrial_date"], errors="coerce")
    df = df.dropna(subset=["terrestrial_date"])

    df = df.drop_duplicates()
    df = df.sort_values("terrestrial_date").reset_index(drop=True)

    for col in ["min_temp", "max_temp", "pressure", "wind_speed", "sol", "ls"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(axis=1, how="all")

    df["avg_temp"] = (df["min_temp"] + df["max_temp"]) / 2
    df["temp_range"] = df["max_temp"] - df["min_temp"]
    df["year"] = df["terrestrial_date"].dt.year

    if "season" in df.columns:
        df["mars_month"] = (df["season"].astype(str)
                            .str.extract(r"(\d+)")[0].astype(float))

    df = df.dropna(subset=["min_temp", "max_temp", "pressure"])
    return df