import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------------
# STEP 1: Load SIPRI Excel File
# ------------------------
df = pd.read_excel(
    'sipri_data_1949_2024.xlsx',
    sheet_name='Constant (2023) US$',
    skiprows=5,  # Skip headers in SIPRI sheet
    engine='openpyxl'
)

# ------------------------
# STEP 2: Clean the DataFrame
# ------------------------
df.rename(columns={df.columns[0]: 'Country'}, inplace=True)
df = df[df['Country'].notna()]  # Remove rows with empty country name
df.columns = df.columns.map(str)  # Ensure all column names are strings

# Remove extra columns like 'Notes' or 'Unnamed'
df = df.loc[:, ~df.columns.str.contains('^Unnamed|Notes', case=False)]

# Keep only 'Country' and year columns
year_columns = [col for col in df.columns if col.isdigit() and len(col) == 4]
df_cleaned = df[['Country'] + year_columns]

# ------------------------
# STEP 3: Melt into Long Format
# ------------------------
df_long = pd.melt(df_cleaned,
                  id_vars='Country',
                  var_name='Year',
                  value_name='Expenditure')

# ------------------------
# STEP 4: Clean Expenditure Values
# ------------------------
df_long['Expenditure'] = (
    df_long['Expenditure']
        .replace('..', None)
        .replace(',', '', regex=True)
)

df_long['Expenditure'] = pd.to_numeric(df_long['Expenditure'], errors='coerce')
df_long.dropna(subset=['Expenditure'], inplace=True)
df_long['Year'] = df_long['Year'].astype(int)

# ------------------------
# STEP 5: Plot India and China Expenditure
# ------------------------

# SAFER match: contains name (case insensitive)
china_data = df_long[df_long['Country'].str.contains('China', case=False, na=False)]
us_data = df_long[df_long['Country'].str.contains('United States', case=False, na=False)]

# Plot U.S.
if not us_data.empty:
    sns.lineplot(x='Year', y='Expenditure', data=us_data, marker='o')
    plt.title('United States Military Expenditure Over Time')
    plt.xlabel('Year')
    plt.ylabel('Expenditure (2023 USD - millions)')
    plt.tight_layout()
    plt.show()
else:
    print("🚫 No data found for 'United States'.")

#Plot China
if not china_data.empty:
    sns.lineplot(x="Year", y="Expenditure", data = china_data, marker = 'o')
    plt.title("China Military Expenditure Over Time")
    plt.xlabel("Year")
    plt.ylabel("Expenditure (2023 USD - millions)")
    plt.tight_layout()
    plt.show()
else:
    print("🚫 No data found for 'China'.")

# Step 1: Combine the data for both countries into one dataframe
# You can use `pd.concat()` to stack the data
combined_data = pd.concat([us_data, china_data])

# Step 2: Plot both countries on the same graph
plt.figure(figsize=(10, 6))  # Optional: Adjust the size of the plot
sns.lineplot(x='Year', y='Expenditure', data=combined_data, hue='Country', marker='o')

# Adding title and labels
plt.title('Military Expenditure Comparison: US vs China')
plt.xlabel('Year')
plt.ylabel('Expenditure (in Millions)')

# Show the plot
plt.show()