import pandas as pd

# Load from clean sheet
df = pd.read_excel(
    'sipri_data_1949_2024.xlsx',
    sheet_name='Constant (2023) US$',
    skiprows=5,
    engine='openpyxl'
)

# Clean
df.rename(columns={df.columns[0]: 'Country'}, inplace=True)
df = df[df['Country'].notna()]

# Show basic preview
print("✅ Data loaded.")
print("Shape:", df.shape)
print("Columns:", df.columns[:10])  # Show first 10 columns
print(df.head(5))  # Show first 5 rows