from tabulate import tabulate
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

data = [
    ["Dependent Variable", "", ""],
    ["", "Δln_exports", "Difference of natural log of exports in million USD (Monthly)."],
    ["", "Δln_imports", "Difference of natural log of imports in million USD (Monthly)."],
    ["Independent Variables", "", ""],
    ["", "official_exchange_rate_percent_change", "Monthly percent change in official exchange rate (LCU/USD)."],
    ["", "REER_percent_change", "Monthly percent change in real effective exchange rate."],
    ["", "official_exchange_rate_percent_changeₜ₋₁", "Monthly percent change in official exchange rate from previous month (LCU/USD)."],
    ["Controls", "", ""],
    ["", "ln_exportsₜ₋₁/ln_importsₜ₋₁", "Lagged value of natural log exports/imports from previous month."],
    ["", "CPI_percent_change", "Monthly inflation rate."],
    ["", "ln_labor", "Natural log of labor input."],
    ["", "GDP_annual_growth", "Annual GDP growth rate."],
    ["", "GDP_per_capita_annual_growth", "Annual GDP per capita growth rate."],
    ["", "export/import_share_of_GDP", "Percent export/import share of GDP (Annual)."],
    ["", "unemployment_rate", "Unemployment rate (% of labor force) (Annual)."],
    ["", "winter", "Seasonal fixed effects for winter,"],
    ["", "spring", "Seasonal fixed effects for spring,"],
    ["", "summer", "Seasonal fixed effects for summer,"],
]

df = pd.DataFrame(data, columns=["Variable Group", "Variable", "Definition"])

# Generate tabulate table as plain text
table_text = tabulate(df, headers='keys', tablefmt='grid')

# Load monospaced font
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 16)  # Adjust path if needed

# Prepare image size
lines = table_text.split('\n')
line_height = font.getbbox('A')[3] - font.getbbox('A')[1]
max_width = max([font.getbbox(line)[2] for line in lines])

padding = 20
image_width = max_width + padding * 2
image_height = line_height * len(lines) + padding * 2

# Create white background image
image = Image.new('RGB', (image_width, image_height), color='white')
draw = ImageDraw.Draw(image)

# Draw text line by line
y_text = padding
for line in lines:
    draw.text((padding, y_text), line, font=font, fill='black')
    y_text += line_height

# Save image
image.save('data/variable_description_table.png')