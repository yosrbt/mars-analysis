import os
import matplotlib.pyplot as plt
from clean import load_data

os.makedirs("images", exist_ok=True)
df = load_data()

cols = ["min_temp", "max_temp", "avg_temp", "pressure"]

# --- Statistiques ---
print("=== Statistiques globales ===")
print(df[cols].describe().round(1))

print("\n=== Corrélations ===")
print(df[cols].corr().round(2))

has_month = "mars_month" in df.columns
if has_month:
    by_month = df.groupby("mars_month")[cols].mean()
    print("\n=== Moyennes par mois martien ===")
    print(by_month.round(1))

print("\n=== Moyennes par année terrestre ===")
print(df.groupby("year")[cols].mean().round(1))

# --- 1. Températures dans le temps ---
plt.figure(figsize=(11, 4))
plt.plot(df["terrestrial_date"], df["max_temp"], label="Max", alpha=0.7)
plt.plot(df["terrestrial_date"], df["min_temp"], label="Min", alpha=0.7)
plt.xlabel("Date")
plt.ylabel("Température (°C)")
plt.title("Températures sur Mars (Curiosity)")
plt.legend()
plt.tight_layout()
plt.savefig("images/temperature_over_time.png", dpi=150)
plt.close()

# --- 2 et 3. Cycles saisonniers ---
if has_month:
    by_month["avg_temp"].plot(kind="bar", figsize=(9, 4))
    plt.xlabel("Mois martien")
    plt.ylabel("Température moyenne (°C)")
    plt.title("Cycle saisonnier de la température")
    plt.tight_layout()
    plt.savefig("images/temp_by_month.png", dpi=150)
    plt.close()

    by_month["pressure"].plot(kind="line", marker="o", figsize=(9, 4))
    plt.xlabel("Mois martien")
    plt.ylabel("Pression (Pa)")
    plt.title("Cycle saisonnier de la pression")
    plt.tight_layout()
    plt.savefig("images/pressure_by_month.png", dpi=150)
    plt.close()

# --- 4. Pression vs température ---
plt.figure(figsize=(6, 5))
plt.scatter(df["pressure"], df["avg_temp"], s=8, alpha=0.5)
plt.xlabel("Pression (Pa)")
plt.ylabel("Température moyenne (°C)")
plt.title("Pression vs température")
plt.tight_layout()
plt.savefig("images/pressure_vs_temp.png", dpi=150)
plt.close()

print("\nGraphiques enregistrés dans images/")