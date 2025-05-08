import pandas as pd
from IPython.display import display
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col

analysis_df = pd.read_excel("data/EU_analysis_data.xlsx")
# print(analysis_df.groupby("Country Code").apply(lambda x: x.isnull().sum().sum()))
# Remove all countries that uses EUR, except for BEL (Belgium)
# analysis_df = analysis_df[~analysis_df['Country Code'].isin(["DEU", "ESP", "FIN","IRL", "ITA", "LUX", "NLD", "PRT",])]
analysis_df = analysis_df.reset_index()
analysis_df = analysis_df.set_index(["Country Code", "Time"])


# Specify the independent variables.
# Adjust the variable names to match your actual DataFrame columns.
exog_vars = ["Lag Official Exchange Rate percent change", 'CPI Price, % y-o-y, not seas. adj.,, [CPTOTSAXNZGY]', 'ln_Labor', "GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]", "GDP per capita growth (annual %) [NY.GDP.PCAP.KD.ZG]", "Exports of goods and services (% of GDP) [NE.EXP.GNFS.ZS]", "Unemployment, total (% of total labor force) (modeled ILO estimate) [SL.UEM.TOTL.ZS]", "Winter", "Spring", "Summer", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]

# # print("STD and Corr 1:")
# # print(analysis_df.groupby("Country Code")[exog_vars].std())
# # print(analysis_df[exog_vars].corr())

# Create the exogenous DataFrame and add a constant.
exog = analysis_df[exog_vars]

exog.columns = ['lag_official_exchange_rate_percent_change', 'CPI_percent_change','ln_labor', 'GDP_annual_growth', 'GDP_per_capita_annual_growth', 'export_share_of_GDP', 'unemployment_rate', 'winter', 'spring', 'summer', "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]

exog = sm.add_constant(exog)

# Define the dependent variable.
dep = analysis_df['ln_exports_change']

# Run the PanelOLS model with entity (country) and time fixed effects.
model = PanelOLS(
    dependent=dep, 
    exog=exog, 
    entity_effects=True
)
results = model.fit(cov_type='clustered', cluster_entity=True)
print(results.summary)

exog_vars_2 = ["Lag Official Exchange Rate percent change", 'CPI Price, % y-o-y, not seas. adj.,, [CPTOTSAXNZGY]', 'ln_Labor', "GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]", "GDP per capita growth (annual %) [NY.GDP.PCAP.KD.ZG]", "Imports of goods and services (% of GDP) [NE.IMP.GNFS.ZS]", "Unemployment, total (% of total labor force) (modeled ILO estimate) [SL.UEM.TOTL.ZS]", "Winter", "Spring", "Summer", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]

# Create the exogenous DataFrame and add a constant.
exog_2 = analysis_df[exog_vars_2]

exog_2.columns = ['lag_official_exchange_rate_percent_change', 'CPI_percent_change','ln_labor', 'GDP_annual_growth', 'GDP_per_capita_annual_growth', 'import_share_of_GDP', 'unemployment_rate', 'winter', 'spring', 'summer', "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"]

exog_2 = sm.add_constant(exog_2)

# Define the dependent variable.
dep_2 = analysis_df['ln_imports_change']

# Run the PanelOLS model with entity (country) and time fixed effects.
model_2 = PanelOLS(
    dependent=dep_2, 
    exog=exog_2, 
    entity_effects=True
)
results_2 = model_2.fit(cov_type='clustered', cluster_entity=True)
print(results_2.summary)


with open("results/exports_robustness_check_summary.txt", "w") as f:
    f.write(results.summary.as_text())

fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, results.summary.as_text(), fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/exports_robustness_check_summary.png", bbox_inches='tight', dpi=300)



with open("results/imports_robustness_check_summary.txt", "w") as f:
    f.write(results_2.summary.as_text())

fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, results_2.summary.as_text(), fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/imports_robustness_check_summary.png", bbox_inches='tight', dpi=300)



def format_result(coef, std, pval):
    if pd.isna(coef):
        return ""  # Blank for missing vars
    stars = '***' if pval < 0.01 else '**' if pval < 0.05 else '*' if pval < 0.1 else ''
    return f"\\makecell{{{coef:.3f}{stars} \\\\ ({std:.3f})}}"

# Keep order as in results
all_vars = [
    'const',
    'lag_official_exchange_rate_percent_change',
    'CPI_percent_change',
    'ln_labor',
    'GDP_annual_growth',
    'GDP_per_capita_annual_growth',
    'export_share_of_GDP', 'import_share_of_GDP',
    'unemployment_rate',
]


# Prepare table
summary_table = pd.DataFrame(index=all_vars)
summary_table['(1)'] = [format_result(results.params.get(v, float('nan')), results.std_errors.get(v, float('nan')), results.pvalues.get(v, float('nan'))) for v in all_vars]
summary_table['(2)'] = [format_result(results_2.params.get(v, float('nan')), results_2.std_errors.get(v, float('nan')), results_2.pvalues.get(v, float('nan'))) for v in all_vars]

summary_table.columns = ['(1)', '(2)']
# Escape only index (variable names)
summary_table.index = summary_table.index.str.replace('_', r'\_', regex=False)

top_row = pd.DataFrame({'(1)': ['\\textit{Δln\_exports}'], '(2)': ['\\textit{Δln\_imports}']},
                       index=['\\textit{Dependent Variable}'])

# Concatenate it to the top of your table
summary_table = pd.concat([top_row, summary_table])

summary_table.loc['Observations'] = [results.nobs, results_2.nobs]
summary_table.loc['R-squared'] = [results.rsquared, results_2.rsquared]

latex_table = summary_table.to_latex(escape=False, column_format='lcc')

latex_table = latex_table.replace(
    '\\textit{Dependent Variable} & \\textit{Δln\_exports} & \\textit{Δln\_imports} \\\\',
    ""
)
latex_table = latex_table.replace(
    '\midrule',
    "\\textit{Dependent Variable} & \\textit{Δln\_exports} & \\textit{Δln\_imports} \\\\ \n\midrule"
)




# Save to LaTeX
with open("results/formatted_table_robustness_check.tex", "w") as f:
    f.write(latex_table)
