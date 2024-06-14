import pandas as pd
from collections import Counter

CHOSEN='dream'
ATT='conversation'
POINT_OF_VIEW='Model'
# Function to process each group
def process_group(group):
    response=[]
    for i in range(len(group)):
        response.append(group.iloc[i][ATT])
    if len(response)==0:
        return None,group.iloc[0][POINT_OF_VIEW]
    value_counts = Counter(response)
    most_common_value, _ = value_counts.most_common(1)[0]
    return most_common_value,group.iloc[0][POINT_OF_VIEW]


# Function to read, filter, and concatenate CSVs
def concatenate_csvs(file1, file2, columns):
    # Read the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Filter the DataFrames to use only the specified columns
    df1_filtered = df1[columns]
    df2_filtered = df2[columns]
    
    # Concatenate the filtered DataFrames
    concatenated_df = pd.concat([df1_filtered, df2_filtered], ignore_index=True)
    
    return concatenated_df


columns = ['id', POINT_OF_VIEW, CHOSEN,ATT]
file1 = 'Dream_ChatGPT/Data/models_usable_data.csv'
df1 = pd.read_csv(file1)
result_df = df1[columns]
result_df = result_df[result_df[CHOSEN] == 'V']
result_df = result_df[result_df[ATT] == 'V']
#remove latin, it is not relevant
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
print(counts)
# Display the counts
counts.to_csv(ATT+'.csv')

