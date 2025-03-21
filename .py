import pandas as pd
from IPython.display import display

GEM_df = pd.read_excel("data/EU_monthly_GEM_data.xlsx")
WDI_df = pd.read_excel("data/EU_WDI_data.xlsx")

GEM_df = GEM_df.drop(columns=['Time Code', 'CPI Price, % y-o-y, median weighted, seas. adj., [CPTOTSAXMZGY]', 'Nominal Effective Exchange Rate,,,, [NEER]', 'Real Effective Exchange Rate,,,, [REER]', 'Country'])
WDI_df = WDI_df.drop(columns=['Time Code', 'Country Name'])
WDI_df = WDI_df.rename({"Time": "Year"}, axis=1)

GEM_df = GEM_df.reset_index()
WDI_df = WDI_df.reset_index()


GEM_df['Year'] = GEM_df['Time'].str[:4]
GEM_df['Year'] = GEM_df['Year'].astype(str).str.strip()
GEM_df['Country Code'] = GEM_df['Country Code'].astype(str).str.strip().str.upper()

WDI_df['Year'] = WDI_df['Year'].astype(str).str.strip()
WDI_df['Country Code'] = WDI_df['Country Code'].astype(str).str.strip().str.upper()

df = pd.merge(GEM_df, WDI_df, on=["Year", "Country Code"], how="left")

print(GEM_df[['Year', 'Country Code']].dtypes)
print(WDI_df.reset_index()[['Year', 'Country Code']].dtypes)

# print("GEM_df index:", GEM_df.index)
# print("GEM_df columns:", GEM_df.columns)

# print("WDI_df index:", WDI_df.index)
# print("WDI_df columns:", WDI_df.columns)

display(df.head(3))
# df.to_excel("data/EU_Joined_data.xlsx")