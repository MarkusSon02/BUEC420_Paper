import pandas as pd
import matplotlib.pyplot as plt

def plot_exports(df, country_code, time_col='Time', export_col='Exports Merchandise, Customs, current US$, millions, not seas. adj. [DXGSRMRCHNSCD]'):
    country_df = df[df['Country Code'] == country_code].copy()
    country_df = country_df.sort_values(by=time_col)
    
    plt.figure(figsize=(12, 6))
    plt.plot(country_df[time_col], country_df[export_col], marker='o', linestyle='-')
    plt.title(f"Exports Over Time – {country_code}")
    plt.xlabel("Time")
    plt.ylabel("Exports (in millions USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(f"data/exports_{country_code}.png")
    plt.close()

def plot_imports(df, country_code, time_col='Time', import_col='Imports Merchandise, Customs, current US$, millions, not seas. adj. [DMGSRMRCHNSCD]'):
    country_df = df[df['Country Code'] == country_code].copy()
    country_df = country_df.sort_values(by=time_col)
    
    plt.figure(figsize=(12, 6))
    plt.plot(country_df[time_col], country_df[import_col], marker='o', linestyle='-', color='green')
    plt.title(f"Imports Over Time – {country_code}")
    plt.xlabel("Time")
    plt.ylabel("Imports (in millions USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(f"data/imports_{country_code}.png")
    plt.close()


df = pd.read_excel("data/EU_cleaned_data.xlsx")
plot_exports(df, 'BEL')
plot_imports(df, 'BEL')
