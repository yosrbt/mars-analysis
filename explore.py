import pandas as pd

df = pd.read_csv("data/mars_weather.csv")
print(df.head())
print()
print(df.info())
print()
print(df.isna().sum())