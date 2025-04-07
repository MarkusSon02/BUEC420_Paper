import pandas as pd
from IPython.display import display
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import numpy as np
import matplotlib.pyplot as plt

analysis_df = pd.read_excel("data/EU_analysis_data.xlsx")
analysis_df = analysis_df.reset_index()
analysis_df = analysis_df.set_index(["Country Code", "Time"])

# Specify the independent variables.
# Adjust the variable names to match your actual DataFrame columns.
exog_vars = ["Official Exchange Rate percent change", 'CPI Price, % y-o-y, not seas. adj.,, [CPTOTSAXNZGY]', 'ln_Labor', "GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]", "GDP per capita growth (annual %) [NY.GDP.PCAP.KD.ZG]", "Exports of goods and services (% of GDP) [NE.EXP.GNFS.ZS]",  "Unemployment, total (% of total labor force) (modeled ILO estimate) [SL.UEM.TOTL.ZS]", "Winter", "Spring", "Summer"]

# # print("STD and Corr 1:")
# # print(analysis_df.groupby("Country Code")[exog_vars].std())
# # print(analysis_df[exog_vars].corr())

# Create the exogenous DataFrame and add a constant.
exog = analysis_df[exog_vars]

exog.columns = ['official_exchange_rate_percent_change', 'CPI_percent_change', 'ln_labor', 'GDP_anual_growth', 'GDP_per_capita_annual_growth', 'export_share_of_GDP', 'unemployment_rate', 'winter', 'spring', 'summer']

exog = sm.add_constant(exog)

# Define the dependent variable.
dep = analysis_df["ln_exports_change"]

# Run the PanelOLS model with entity (country) and time fixed effects.
model = PanelOLS(
    dependent=dep, 
    exog=exog, 
    entity_effects=True
)
results = model.fit(cov_type='clustered', cluster_entity=True)
print(results.summary)



exog_vars_2 = ["Official Exchange Rate percent change", 'CPI Price, % y-o-y, not seas. adj.,, [CPTOTSAXNZGY]', 'ln_Labor', "GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]", "GDP per capita growth (annual %) [NY.GDP.PCAP.KD.ZG]", "Imports of goods and services (% of GDP) [NE.IMP.GNFS.ZS]", "Unemployment, total (% of total labor force) (modeled ILO estimate) [SL.UEM.TOTL.ZS]", "Winter", "Spring", "Summer"]

# Create the exogenous DataFrame and add a constant.
exog_2 = analysis_df[exog_vars_2]

exog_2.columns = ['official_exchange_rate_percent_change', 'CPI_percent_change', 'ln_labor', 'GDP_anual_growth', 'GDP_per_capita_annual_growth', 'import_share_of_GDP', 'unemployment_rate', 'winter', 'spring', 'summer']

exog_2 = sm.add_constant(exog_2)

# Define the dependent variable.
dep_2 = analysis_df["ln_imports_change"]

# Run the PanelOLS model with entity (country) and time fixed effects.
model_2 = PanelOLS(
    dependent=dep_2, 
    exog=exog_2, 
    entity_effects=True
)
results_2 = model_2.fit(cov_type='clustered', cluster_entity=True)
print(results_2.summary)


with open("results/exports_new_regression_2_summary.txt", "w") as f:
    f.write(results.summary.as_text())

# Create the figure
fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, results.summary.as_text(), fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/exports_new_regression_2_summary.png", bbox_inches='tight', dpi=300)



with open("results/imports_new_regression_2_summary.txt", "w") as f:
    f.write(results_2.summary.as_text())

fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, results_2.summary.as_text(), fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/imports_new_regression_2_summary.png", bbox_inches='tight', dpi=300)