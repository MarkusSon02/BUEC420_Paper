import pandas as pd

data = pd.read_stata("asia-industry_tidy.dta")
data.to_excel("asia-industry_tidy.xlsx")
data = pd.read_stata("usa-imports.dta")
data.to_excel("usa-imports.xlsx")