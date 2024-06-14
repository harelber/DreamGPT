import pandas as pd
import sys
# Step 1: Read the CSV file into a Pandas DataFrame
file_path = sys.argv[1]  # replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv(file_path)

# Step 2: Format the DataFrame to show only two digits after the decimal point
df = df.applymap(lambda x: f'{x:.2f}' if isinstance(x, (float, int)) else x)

# Step 2: Convert the DataFrame to a LaTeX table
latex_table = df.to_latex(index=False)

# Step 3: Save the LaTeX table to a .tex file
with open(sys.argv[1]+'_latex_table.tex', 'w') as f:
    f.write(latex_table)

print("LaTeX table has been saved to table.tex")