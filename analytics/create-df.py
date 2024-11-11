#%%
import sqlite3
import pandas as pd
import os

# Path to the database
db_path = os.path.join('data', 'bergamoto.db')

# Connect to the database
conn = sqlite3.connect(db_path)

# Create a cursor object
cursor = conn.cursor()

# Example query
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch and print the results
tables = cursor.fetchall()
print("Tables in the database:", tables)

# Query to select all data from the 'horarios' table
query = "SELECT * FROM horarios"

# Execute the query and load the data directly into a DataFrame
df_horarios = pd.read_sql_query(query, conn)

# Print the DataFrame
print(df_horarios)

#%%
# Close the connection
conn.close()

# Exclude the 'photo' column if it exists
if 'photo' in df_horarios.columns:
    df_horarios = df_horarios.drop(columns=['photo'])

# Ensure 'pin' column is treated as text
df_horarios['pin'] = df_horarios['pin'].astype(str)

# Save the DataFrame to a CSV file with UTF-8 encoding
csv_path = os.path.join('data', 'horarios-ds.csv')
df_horarios.to_csv(csv_path, index=False, encoding='utf-8')
