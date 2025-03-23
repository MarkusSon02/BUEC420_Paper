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
GEM_df['Time'] = GEM_df['Time'].astype(str)
GEM_df["Year"] = pd.to_numeric(GEM_df["Year"], errors='coerce')
GEM_df['Country Code'] = GEM_df['Country Code'].astype(str)
WDI_df["Year"] = pd.to_numeric(WDI_df["Year"], errors='coerce')
WDI_df['Country Code'] = WDI_df['Country Code'].astype(str)

df = pd.merge(GEM_df, WDI_df, on=["Year", "Country Code"], how="left")

# print(GEM_df[['Year', 'Country Code']].dtypes)
# print(WDI_df.reset_index()[['Year', 'Country Code']].dtypes)

# print("GEM_df index:", GEM_df.index)
# print("GEM_df columns:", GEM_df.columns)

# print("WDI_df index:", WDI_df.index)
# print("WDI_df columns:", WDI_df.columns)

count_countries = df["Country Code"].value_counts()
print(len(count_countries))
display(df.head(3))
# df.to_excel("data/EU_Joined_data.xlsx")


for col in df.columns:
    if col not in ["Time", "Country Code"]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df['Time'] = df['Time'].astype("string")
df['Country Code'] = df['Country Code'].astype("string")


df = df[~df['Country Code'].isin(['EST', 'MLT', 'LTU'])]
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df[df['Year'] > 1993]
df = df[df['Time'] < "2024M04"]
df = df.sort_values(by=["Country Code", "Time"])



print(df.isna().sum().sum())

# count_countries = df["Country Code"].value_counts()
# print(len(count_countries))

df = df.groupby(["Country Code"], as_index=False).ffill()
df = df.reset_index()
print(df.dtypes)
df.to_excel("data/EU_cleaned_data.xlsx", index=False)

print(df.isna().sum().sum())
display(df.head(3))