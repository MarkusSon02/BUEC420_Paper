import pandas as pd
from IPython.display import display
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import numpy as np
import matplotlib.pyplot as plt

GEM_df = pd.read_excel("data/EU_GEM_data.xlsx")
WDI_df = pd.read_excel("data/EU_WDI_data.xlsx")

GEM_df = GEM_df.drop(columns=['Time Code', 'CPI Price, % y-o-y, median weighted, seas. adj., [CPTOTSAXMZGY]', 'Exports Merchandise, Customs, current US$, millions, seas. adj. [DXGSRMRCHSACD]', 'Imports Merchandise, Customs, current US$, millions, seas. adj. [DMGSRMRCHSACD]', 'Industrial Production, constant US$, seas. adj.,, [IPTOTSAKD]'])
WDI_df = WDI_df.drop(columns=['Time Code', 'Country Name', "Educational attainment, at least Master's or equivalent, population 25+, total (%) (cumulative) [SE.TER.CUAT.MS.ZS]", "Educational attainment, Doctoral or equivalent, population 25+, total (%) (cumulative) [SE.TER.CUAT.DO.ZS]", "Educational attainment, at least Bachelor's or equivalent, population 25+, total (%) (cumulative) [SE.TER.CUAT.BA.ZS]", "Educational attainment, at least completed lower secondary, population 25+, total (%) (cumulative) [SE.SEC.CUAT.LO.ZS]", "Educational attainment, at least completed post-secondary, population 25+, total (%) (cumulative) [SE.SEC.CUAT.PO.ZS]", "Educational attainment, at least completed primary, population 25+ years, total (%) (cumulative) [SE.PRM.CUAT.ZS]", "Educational attainment, at least completed short-cycle tertiary, population 25+, total (%) (cumulative) [SE.TER.CUAT.ST.ZS]", "Educational attainment, at least completed upper secondary, population 25+, total (%) (cumulative) [SE.SEC.CUAT.UP.ZS]",])
WDI_df = WDI_df.rename({"Time": "Year"}, axis=1)

GEM_df = GEM_df.reset_index(drop=True)
WDI_df = WDI_df.reset_index(drop=True)

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
# print(len(count_countries))
# display(df.head(3))
# df.to_excel("data/EU_Joined_data.xlsx")

joined_df = df

for col in joined_df.columns:
    if col not in ["Time", "Country Code", "Country"]:
        joined_df[col] = pd.to_numeric(joined_df[col], errors='coerce')

joined_df['Time'] = joined_df['Time'].astype("string")
joined_df['Country Code'] = joined_df['Country Code'].astype("string")
joined_df['Country'] = joined_df['Country'].astype("string")


joined_df = joined_df[~joined_df['Country Code'].isin(['EST', 'MLT', 'LTU', 'HRV', 'CYP', 'CZE', 'GRC', 'SVK', 'AUT', 'FRA', 'HUN', 'YUG', 'CHE', 'GEO', 'RUS', 'BGR', 'SVN', 'DNK', 'ISL', 'GBR'])]
joined_df = joined_df[~joined_df['Country Code'].isin(['ARE', 'ARG', 'AUS', 'BRA', 'JPN', 'MYS', 'NZL', 'PHL'])]
joined_df['Year'] = pd.to_numeric(joined_df['Year'], errors='coerce')
joined_df = joined_df[joined_df['Year'] > 2009]
joined_df = joined_df[joined_df['Year'] < 2019]
joined_df = joined_df.sort_values(by=["Country Code", "Time"])
joined_df['Month'] = joined_df["Time"].str[-2:]
joined_df['Month'] = pd.to_numeric(joined_df['Month'], errors='coerce')
joined_df['Time'] = pd.to_datetime(joined_df['Time'].str.replace('M', '-') + '-01', errors='coerce')


print("Count of null values: ", joined_df.isna().sum().sum())

count_countries = joined_df["Country Code"].value_counts()
print("Number of countries:", len(count_countries))
joined_df.to_excel("data/EU_semi_cleaned_data.xlsx", index=False)

for col in joined_df.columns:
    joined_df[col] = joined_df.groupby(["Country Code"])[col].ffill()


joined_df = joined_df.reset_index()
# print(joined_df.dtypes)
joined_df.to_excel("data/EU_cleaned_data.xlsx", index=False)


print(joined_df.isna().sum().sum())
# print("\n\n\n\n\n")
print(joined_df.shape)
print(joined_df.groupby("Country Code").apply(lambda x: x.isnull().sum().sum()))
# display(joined_df.head(3))

analysis_df = joined_df

# Calculate net exports if not already computed
# analysis_df.columns = ['index', 'Time', 'Country', 'Country Code', 'CPI Price', 'Exports, not seas. adj', 'Exports, seas. adj', 'Imports, not seas. adj', 'Imports, seas. adj', 'Industrial Production, not seas. adj', 'Industrial Production, seas. adj', 'Official exchange rate', 'Year', 'Labor force', 'Labor force participation rate ILO estimate', 'Labor force participation rate national estimate', 'Labor force with advanced education', 'Labor force with basic education', 'Labor force with intermediate education', ]
# analysis_df['Net Exports seas. adj'] = analysis_df['Exports Merchandise, Customs, current US$, millions, seas. adj. [DXGSRMRCHSACD]'] - analysis_df['Imports Merchandise, Customs, current US$, millions, seas. adj. [DMGSRMRCHSACD]']
analysis_df['Net Exports not seas. adj'] = analysis_df['Exports Merchandise, Customs, current US$, millions, not seas. adj. [DXGSRMRCHNSCD]'] - analysis_df['Imports Merchandise, Customs, current US$, millions, not seas. adj. [DMGSRMRCHNSCD]']
# analysis_df['Lag Net Exports seas. adj'] = analysis_df.groupby("Country Code")['Net Exports seas. adj'].shift(1)
analysis_df['Lag Net Exports not seas. adj'] = analysis_df.groupby("Country Code")['Net Exports not seas. adj'].shift(1)
analysis_df['Lag Exports not seas. adj'] = analysis_df.groupby("Country Code")['Exports Merchandise, Customs, current US$, millions, not seas. adj. [DXGSRMRCHNSCD]'].shift(1)
analysis_df['Lag Imports not seas. adj'] = analysis_df.groupby("Country Code")['Imports Merchandise, Customs, current US$, millions, not seas. adj. [DMGSRMRCHNSCD]'].shift(1)
analysis_df["Official exchange rate percent change"] = analysis_df.groupby("Country Code")["Official exchange rate, LCU per USD, period average,, [DPANUSLCU]"].pct_change() * 100
analysis_df["Nominal Effective Exchange Rate percent change"] = analysis_df.groupby("Country Code")["Nominal Effective Exchange Rate,,,, [NEER]"].pct_change() * 100
analysis_df["Real Effective Exchange Rate percent change"] = analysis_df.groupby("Country Code")["Real Effective Exchange Rate,,,, [REER]"].pct_change() * 100
analysis_df["Net Exports percent change"] = analysis_df.groupby("Country Code")["Net Exports not seas. adj"].pct_change() * 100
analysis_df.reset_index()
# analysis_df = analysis_df.dropna(subset=['Lag Net Exports seas. adj', 'Lag Net Exports not seas. adj', "Official exchange rate percent change"])

# analysis_df['ln_Net_Exports seas. adj'] = np.log(analysis_df['Net Exports seas. adj'])
# analysis_df['ln_Net_Exports not seas. adj'] = np.log(analysis_df['Net Exports not seas. adj'])
# analysis_df['ln_Lag_Net_Exports seas.adj'] = np.log(analysis_df['Lag Net Exports seas. adj'])
# analysis_df['ln_Lag_Net_Exports not seas. adj'] = np.log(analysis_df['Lag Net Exports not seas. adj'])
analysis_df['ln_Labor'] = np.log(analysis_df['Labor force, total [SL.TLF.TOTL.IN]'])
# analysis_df['ln_Industial_Production seas. adj'] = np.log(analysis_df['Industrial Production, constant US$, seas. adj.,, [IPTOTSAKD]'])
analysis_df['ln_Industial_Production not seas. adj'] = np.log(analysis_df['Industrial Production, constant US$,,, [IPTOTNSKD]'])
analysis_df['ln_GDP'] = np.log(analysis_df['GDP (current US$) [NY.GDP.MKTP.CD]'])
analysis_df['ln_GDP_per_capita'] = np.log(analysis_df['GDP per capita (current US$) [NY.GDP.PCAP.CD]'])
analysis_df['ln_exports'] = np.log(analysis_df['Exports Merchandise, Customs, current US$, millions, not seas. adj. [DXGSRMRCHNSCD]'])
analysis_df['ln_imports'] = np.log(analysis_df['Imports Merchandise, Customs, current US$, millions, not seas. adj. [DMGSRMRCHNSCD]'])
analysis_df['ln_lag_exports'] = np.log(analysis_df['Lag Exports not seas. adj'])
analysis_df['ln_lag_imports'] = np.log(analysis_df['Lag Imports not seas. adj'])

analysis_df['Season'] = 'Winter'
analysis_df.loc[(analysis_df['Month'] >= 3) & (analysis_df['Month'] <= 5), 'Season'] = 'Spring'
analysis_df.loc[(analysis_df['Month'] >= 6) & (analysis_df['Month'] <= 8), 'Season'] = 'Summer'
analysis_df.loc[(analysis_df['Month'] >= 9) & (analysis_df['Month'] <= 11), 'Season'] = 'Autumn'
season_dummies = pd.get_dummies(analysis_df['Season'], drop_first=True)
analysis_df = pd.concat([analysis_df, season_dummies], axis=1)

display(season_dummies.head(3))
# Set the MultiIndex for panel data: Country Code and Time
analysis_df = analysis_df.set_index(["Country Code", "Time"])
analysis_df.to_excel("data/EU_analysis_data.xlsx")

# plt.scatter(analysis_df['Official exchange rate percent change'])
# plt.title('Scatterplot for Official exchange rate percent change')
# plt.ylabel('Official exchange rate percent change')
# plt.savefig('results/official_exchange_rate_percent_change_boxplot.png')

# plt.scatter(analysis_df['Real Effective Exchange Rate percent change'])
# plt.title('Scatterplot for Real Effective Exchange Rate percent change')
# plt.ylabel('Real Effective Exchange Rate percent change')
# plt.savefig('results/real_exchange_rate_percent_change_boxplot.png')

# plt.scatter(analysis_df['Nominal Effective Exchange Rate percent change'])
# plt.title('Scatterplot for Nominal Effective Exchange Rate percent change')
# plt.ylabel('Nominal Effective Exchange Rate percent change')
# plt.savefig('results/nominal_exchange_rate_percent_change_boxplot.png')

Q1 = analysis_df['Official exchange rate percent change'].quantile(0.25)
Q3 = analysis_df['Official exchange rate percent change'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

analysis_df = analysis_df[(analysis_df['Official exchange rate percent change'] > lower_bound) & (analysis_df['Official exchange rate percent change'] < upper_bound)]



# Specify the independent variables.
# Adjust the variable names to match your actual DataFrame columns.
exog_vars = ['ln_lag_exports', "Official exchange rate percent change", 'CPI Price, % y-o-y, not seas. adj.,, [CPTOTSAXNZGY]', 'ln_Industial_Production not seas. adj', 'ln_Labor', "GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]", "GDP per capita growth (annual %) [NY.GDP.PCAP.KD.ZG]", "Winter", "Spring", "Summer"]

# # print("STD and Corr 1:")
# # print(analysis_df.groupby("Country Code")[exog_vars].std())
# # print(analysis_df[exog_vars].corr())

# Create the exogenous DataFrame and add a constant.
exog = analysis_df[exog_vars]
exog = sm.add_constant(exog)

# Define the dependent variable.
dep = analysis_df['ln_exports']

# Run the PanelOLS model with entity (country) and time fixed effects.
model = PanelOLS(
    dependent=dep, 
    exog=exog, 
    entity_effects=True
)
results = model.fit(cov_type='clustered', cluster_entity=True)
print(results.summary)

exog_vars_2 = ['Lag Net Exports not seas. adj', "Official exchange rate percent change", 'CPI Price, % y-o-y, not seas. adj.,, [CPTOTSAXNZGY]', 'ln_Labor', "GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]", "GDP per capita growth (annual %) [NY.GDP.PCAP.KD.ZG]", "Exports of goods and services (% of GDP) [NE.EXP.GNFS.ZS]", "Imports of goods and services (% of GDP) [NE.IMP.GNFS.ZS]", "Unemployment, total (% of total labor force) (modeled ILO estimate) [SL.UEM.TOTL.ZS]","Winter", "Spring", "Summer"]

# with open("results/STD_Corr_2.txt", "w") as f:
#     f.write("Standard Deviation by Country:\n")
#     std_text = analysis_df.groupby("Country Code")[exog_vars_2].std().to_string()
#     f.write(std_text)
#     f.write("\n\nCorrelation Matrix:\n")
#     corr_text = analysis_df[exog_vars_2].corr().to_string()
#     f.write(corr_text)

# # print("STD and Corr 2:")
# # print(analysis_df.groupby("Country Code")[exog_vars_2].std())
# # print(analysis_df[exog_vars_2].corr())

# Create the exogenous DataFrame and add a constant.
exog_2 = analysis_df[exog_vars_2]
exog_2 = sm.add_constant(exog_2)

# Define the dependent variable.
dep_2 = analysis_df['Net Exports not seas. adj']

# Run the PanelOLS model with entity (country) and time fixed effects.
model_2 = PanelOLS(
    dependent=dep_2, 
    exog=exog_2, 
    entity_effects=True
)
results_2 = model_2.fit(cov_type='clustered', cluster_entity=True)
print(results_2.summary)

exog_vars_3 = ['Lag Net Exports not seas. adj', "Real Effective Exchange Rate,,,, [REER]", "Official exchange rate, LCU per USD, period average,, [DPANUSLCU]", 'CPI Price, % y-o-y, not seas. adj.,, [CPTOTSAXNZGY]', 'ln_Labor', "GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]", "GDP per capita growth (annual %) [NY.GDP.PCAP.KD.ZG]", "Exports of goods and services (% of GDP) [NE.EXP.GNFS.ZS]", "Imports of goods and services (% of GDP) [NE.IMP.GNFS.ZS]", "Unemployment, total (% of total labor force) (modeled ILO estimate) [SL.UEM.TOTL.ZS]","Winter", "Spring", "Summer"]

with open("results/STD_Corr_2.txt", "w") as f:
    f.write("Standard Deviation by Country:\n")
    std_text = analysis_df.groupby("Country Code")[exog_vars_3].std().to_string()
    f.write(std_text)
    f.write("\n\nCorrelation Matrix:\n")
    corr_text = analysis_df[exog_vars_3].corr().to_string()
    f.write(corr_text)

# print("STD and Corr 3:")
# print(analysis_df.groupby("Country Code")[exog_vars_3].std())
# print(analysis_df[exog_vars_3].corr())

# Create the exogenous DataFrame and add a constant.
exog_3 = analysis_df[exog_vars_3]
exog_3 = sm.add_constant(exog_3)

# Define the dependent variable.
dep_3 = analysis_df['Net Exports not seas. adj']

# Run the PanelOLS model with entity (country) and time fixed effects.
model_3 = PanelOLS(
    dependent=dep_3, 
    exog=exog_3, 
    entity_effects=True
)
results_3 = model_3.fit(cov_type='clustered', cluster_entity=True)
print(results_3.summary)

with open("results/analysis_summary.txt", "w") as f:
    f.write(results.summary.as_text())
with open("results/analysis_summary_2.txt", "w") as f:
    f.write(results_2.summary.as_text())
with open("results/analysis_summary_3.txt", "w") as f:
    f.write(results_3.summary.as_text())

# print(results.summary)
display(analysis_df.head(3))