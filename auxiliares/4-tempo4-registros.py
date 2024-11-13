#%%
import pandas as pd
import matplotlib.pyplot as plt
#%%
df = pd.read_csv('auxiliares/tempo4-registros.csv', index_col=False, dtype=str, encoding='utf-8')

# Check if 'date' column exists
if 'date' not in df.columns:
	raise KeyError("The 'date' column is not found in the CSV file.")

# %%
# Convert 'total_time' to timedelta and 'date' to datetime
df['total_time'] = pd.to_timedelta(df['total_time'])
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

# Set 'date' as the index
df.set_index('date', inplace=True)

# Resample the data to 7-day intervals and calculate the mean of 'total_time'
mean_time_per_week = df['total_time'].resample('7D').mean()

# Convert mean_time_per_week to hours
mean_time_per_week_hours = mean_time_per_week / pd.Timedelta(hours=1)

# Plot the mean time per week in hours
plt.figure(figsize=(10, 6))
mean_time_per_week_hours.plot(kind='bar')
plt.xlabel('Date')
plt.ylabel('Average Total Time (hours)')
plt.title('Average Total Time per 7 Days')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# %%
