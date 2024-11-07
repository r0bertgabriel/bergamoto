import sqlite3
import pandas as pd

# Path to the database
db_path = 'data/bergamoto.db'

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

# Query to select all data from the 'horarios' table
query = "SELECT * FROM horarios"

# Execute the query and load the data directly into a DataFrame
df_horarios = pd.read_sql_query(query, conn)

# Print the DataFrame
print(df_horarios)

# Close the connection
conn.close()