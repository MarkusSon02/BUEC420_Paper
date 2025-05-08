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

def plot_ln_exports(df, country_code, time_col='Time', export_col='ln_exports'):
    country_df = df[df['Country Code'] == country_code].copy()
    country_df = country_df.sort_values(by=time_col)
    
    plt.figure(figsize=(12, 6))
    plt.plot(country_df[time_col], country_df[export_col], marker='o', linestyle='-')
    plt.title(f"Log Exports Over Time – {country_code}")
    plt.xlabel("Time")
    plt.ylabel("Log Exports")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(f"data/ln_exports_{country_code}.png")
    plt.close()

def plot_ln_imports(df, country_code, time_col='Time', import_col='ln_imports'):
    country_df = df[df['Country Code'] == country_code].copy()
    country_df = country_df.sort_values(by=time_col)
    
    plt.figure(figsize=(12, 6))
    plt.plot(country_df[time_col], country_df[import_col], marker='o', linestyle='-', color='green')
    plt.title(f"Log Imports Over Time – {country_code}")
    plt.xlabel("Time")
    plt.ylabel("Log Imports")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(f"data/ln_imports_{country_code}.png")
    plt.close()

def plot_exports_and_OER(df, export_col='Exports Merchandise, Customs, current US$, millions, not seas. adj. [DXGSRMRCHNSCD]'):
    plt.figure(figsize=(8,6))
    plt.scatter(df["Official Exchange Rate percent change"], df[export_col], alpha=0.6)
    plt.xlabel('Official Exchange Rate Percentage Change')
    plt.ylabel('Exports (Million USD)')
    plt.title('Scatterplot of Exports and Official Exchange Rate')
    plt.grid(True)
    plt.savefig(f"data/exports_OER.png")
    plt.close()

def plot_imports_and_OER(df, import_col='Imports Merchandise, Customs, current US$, millions, not seas. adj. [DMGSRMRCHNSCD]'):
    plt.figure(figsize=(8,6))
    plt.scatter(df["Official Exchange Rate percent change"], df[import_col], alpha=0.6)
    plt.xlabel('Official Exchange Rate Percentage Change')
    plt.ylabel('Imports (Million USD)')
    plt.title('Scatterplot of Imports and Official Exchange Rate')
    plt.savefig(f"data/imports_OER.png")
    plt.close()

def plot_ln_exports_and_OER(df, export_col='ln_exports_change'):
    plt.figure(figsize=(8,6))
    plt.scatter(df["Official Exchange Rate percent change"], df[export_col], alpha=0.6)
    plt.xlabel('Official Exchange Rate Percentage Change')
    plt.ylabel('Log Exports')
    plt.title('Scatterplot of Log Exports and Official Exchange Rate')
    plt.grid(True)
    plt.savefig(f"data/ln_exports_OER.png")
    plt.close()

def plot_ln_imports_and_OER(df, import_col='ln_imports_change'):
    plt.figure(figsize=(8,6))
    plt.scatter(df["Official Exchange Rate percent change"], df[import_col], alpha=0.6)
    plt.xlabel('Official Exchange Rate Percentage Change')
    plt.ylabel('Log Imports')
    plt.title('Scatterplot of Log Imports and Official Exchange Rate')
    plt.savefig(f"data/ln_imports_OER.png")
    plt.close()

df = pd.read_excel("data/EU_cleaned_data.xlsx")
analysis_df = pd.read_excel("data/EU_analysis_data.xlsx")
plot_exports(df, 'BEL')
plot_imports(df, 'BEL')
plot_ln_exports(analysis_df, 'BEL')
plot_ln_imports(analysis_df, 'BEL')
plot_exports_and_OER(analysis_df)
plot_imports_and_OER(analysis_df)
plot_ln_exports_and_OER(analysis_df)
plot_ln_imports_and_OER(analysis_df)
