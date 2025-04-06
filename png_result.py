import matplotlib.pyplot as plt

# Main regression
# Load the regression summary text
with open("permanent_results/exports_main_regression_summary.txt", "r") as file:
    summary_text = file.read()

# Create the figure
fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, summary_text, fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/exports_main_regression_summary.png", bbox_inches='tight', dpi=300)



# Load the regression summary text
with open("permanent_results/imports_main_regression_summary.txt", "r") as file:
    summary_text = file.read()

# Create the figure
fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, summary_text, fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/imports_main_regression_summary.png", bbox_inches='tight', dpi=300)


# Mechanism Analysis
# Load the regression summary text
with open("permanent_results/exports_reer_regression_summary.txt", "r") as file:
    summary_text = file.read()

# Create the figure
fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, summary_text, fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/exports_reer_regression_summary.png", bbox_inches='tight', dpi=300)



# Load the regression summary text
with open("permanent_results/imports_reer_regression_summary.txt", "r") as file:
    summary_text = file.read()

# Create the figure
fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, summary_text, fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/imports_reer_regression_summary.png", bbox_inches='tight', dpi=300)



# Robustness Check
# Load the regression summary text
with open("permanent_results/exports_robustness_check_summary.txt", "r") as file:
    summary_text = file.read()

# Create the figure
fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, summary_text, fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/exports_robustness_check_summary.png", bbox_inches='tight', dpi=300)



# Load the regression summary text
with open("permanent_results/imports_robustness_check_summary.txt", "r") as file:
    summary_text = file.read()

# Create the figure
fig, ax = plt.subplots(figsize=(12, 10))
ax.axis("off")  # Hide axes
fig.patch.set_facecolor('white')  # White background

# Display the text
ax.text(0, 1, summary_text, fontsize=10, family='monospace', va='top')

# Save as image
plt.savefig("png_results/imports_robustness_check_summary.png", bbox_inches='tight', dpi=300)
