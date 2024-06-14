import pandas as pd
from collections import Counter
import json
import scipy.stats as stats
import numpy as np
import math

CHOSEN='dream'
ATT='items'
POINT_OF_VIEW='tag'
DESIRED_VALUES=["flower"]

def check_values(text):
    for val in DESIRED_VALUES:
        try:
            if val in text:
                return True
        except:
            return False
    return False

# Function to perform Chi-square test for each pair of group and language
def chi_square_test(df):
    significant_pairs = []
    for col in df.columns:
        for idx in df.index:
            observed = pd.DataFrame([[df.at[idx, col], df[col].sum() - df.at[idx, col]], 
                                     [df.loc[idx].sum() - df.at[idx, col], df.sum().sum() - df[col].sum() - df.loc[idx].sum() + df.at[idx, col]]])
            chi2, p, _, _ = stats.chi2_contingency(observed)
            if p < 0.05:
                significant_pairs.append((idx, col, p))
    return significant_pairs

# Function to process each group
def process_group(group):
    response=[]
    for i in range(len(group)):
        response.append(check_values(group.iloc[i][ATT]))
            
    value_counts = Counter(response)
    most_common_value, _ = value_counts.most_common(1)[0]
    if most_common_value=="NaN":
        print(group.iloc[i]['id'])
    if type(most_common_value)==float and math.isnan(most_common_value):
        print(group.iloc[i]['id'])
    return most_common_value,group.iloc[0][POINT_OF_VIEW]


file1 = 'Dream_ChatGPT/Data/models_usable_data.csv'
df1 = pd.read_csv(file1)
columns = ['id', POINT_OF_VIEW, CHOSEN,ATT]
result_df = df1[columns]
result_df = result_df[result_df[CHOSEN] == 'V']
result_df = result_df[result_df['tag'].isin(['male', 'female', 'a person'])]
# Group by 'Category' column
grouped =result_df.groupby('id')

# Apply the function to each group
result = grouped.apply(process_group).reset_index()



# Split the 'TupleColumn' into two separate columns
result[[POINT_OF_VIEW, 'value']] = pd.DataFrame(result[0].tolist(), index=result.index)

# Drop the original 'TupleColumn' if no longer needed
df = result.drop(columns=[0])
# Create a crosstab to count occurrences of 'X', 'V', and None for each value in Col1
counts = pd.crosstab(result[POINT_OF_VIEW], result['value'], dropna=False)

# Rename columns for better clarity
counts.columns = ['None' if pd.isna(x) else f'{x}' for x in counts.columns]

#now, run chi square
observed_df=counts

# Perform the Chi-square test for the entire table
chi2, p, dof, expected = stats.chi2_contingency(counts)

# Save observed and expected tables to CSV
observed_df.to_csv("observed_table_langs.csv")
expected_df = pd.DataFrame(expected, columns=counts.columns, index=counts.index)
expected_df.to_csv("expected_table_langs.csv")
resid=open("settings_residulas.csv",'w')

# Output the chi-square test results
resid.write(f"Chi-square statistic: {chi2}\n")
resid.write(f"P-value: {p}\n")
resid.write(f"Degrees of freedom: {dof}\n")


# Calculate standardized residuals
standardized_residuals = (observed_df - expected_df) / np.sqrt(expected_df)
standardized_residuals.to_csv("standardized_residuals.csv")
# Find significant residuals (absolute value greater than 2)

significant_residuals = standardized_residuals.abs() > 2

# Display rows and columns with significant residuals
resid.write("\nSignificant Residuals (Absolute value > 2):\n")
for row in significant_residuals.index:
    for col in significant_residuals.columns:
        if significant_residuals.loc[row, col]:
            resid.write(f"Row: {row}, Column: {col}, Residual: {standardized_residuals.loc[row, col]}\n")