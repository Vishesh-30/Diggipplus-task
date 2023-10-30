import pandas as pd

# Read the JSON file
df = pd.read_json('data.json')

# Convert the JSON file to CSV
df.to_csv('data.csv', index=False)

# Print the first 5 rows of the CSV file
print(df.head())
