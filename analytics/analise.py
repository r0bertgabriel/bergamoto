#%%
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt

#%%
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'horarios-ds.csv')
df = pd.read_csv(file_path, index_col=False, dtype=str, encoding='utf-8')
df
# %%
df['entrada'] = None
df['s-almoco'] = None
df['r-almoco'] = None
df['saida'] = None
df
# %%
def mark_times(group):
    count = group.shape[0]
    if count == 4:
        group.loc[group.index[0], 'entrada'] = True
        group.loc[group.index[1], 's-almoco'] = True
        group.loc[group.index[2], 'r-almoco'] = True
        group.loc[group.index[3], 'saida'] = True
    elif count == 3:
        group.loc[group.index[0], 'entrada'] = True
        group.loc[group.index[1], 's-almoco'] = True
        group.loc[group.index[2], 'r-almoco'] = True
    elif count == 2:
        group.loc[group.index[0], 'entrada'] = True
        group.loc[group.index[1], 'saida'] = True
    return group

df = df.groupby(['name', 'date'], group_keys=False).apply(mark_times)

df['entrada'] = df['entrada'].astype(bool)
df['s-almoco'] = df['s-almoco'].astype(bool)
df['r-almoco'] = df['r-almoco'].astype(bool)
df['saida'] = df['saida'].astype(bool)
#%%
def generate_user_day_hash(pin, date):
    hash_input = f"{pin}{date}".encode('utf-8')
    return hashlib.sha256(hash_input).hexdigest()

def generate_user_month_hash(pin, date):
    month_year = date[3:]  # Assuming date format is DD-MM-YYYY
    hash_input = f"{pin}{month_year}".encode('utf-8')
    return hashlib.sha256(hash_input).hexdigest()

def generate_user_year_hash(pin, date):
    year = date[6:]  # Assuming date format is DD-MM-YYYY
    hash_input = f"{pin}{year}".encode('utf-8')
    return hashlib.sha256(hash_input).hexdigest()

df['user_day_hash'] = df.apply(lambda row: generate_user_day_hash(row['pin'], row['date']), axis=1)
df['user_month_hash'] = df.apply(lambda row: generate_user_month_hash(row['pin'], row['date']), axis=1)
df['user_year_hash'] = df.apply(lambda row: generate_user_year_hash(row['pin'], row['date']), axis=1)
df['setor_day_hash'] = df.apply(lambda row: generate_user_day_hash(row['setor'], row['date']), axis=1)
df['setor_month_hash'] = df.apply(lambda row: generate_user_month_hash(row['setor'], row['date']), axis=1)
df['setor_year_hash'] = df.apply(lambda row: generate_user_year_hash(row['setor'], row['date']), axis=1)
#%%

if (df.groupby(['pin', 'date'])['time'].transform('count') == 4).any():
    df['horas_trabalhadas'] = None

    def calcular_horas_trabalhadas(group):
        if len(group) == 4:
            times = pd.to_datetime(group['time'].sort_values(), format='%H:%M:%S')
            horas_trabalhadas = (times.iloc[1] - times.iloc[0]) + (times.iloc[3] - times.iloc[2])
            group['horas_trabalhadas'] = horas_trabalhadas
        return group

    df = df.groupby(['pin', 'date'], group_keys=False).apply(calcular_horas_trabalhadas).reset_index(drop=True)
    df['horas_trabalhadas'] = df['horas_trabalhadas'].apply(lambda x: str(x)[7:] if pd.notnull(x) else x)
    print(df[['pin', 'date', 'horas_trabalhadas']].drop_duplicates().head(5))
    # Create a new DataFrame with the relevant columns
    df_horas_trabalhadas = df[['pin', 'date', 'horas_trabalhadas']].drop_duplicates().reset_index(drop=True)
    df_horas_trabalhadas

#%%
df_horas_trabalhadas[df_horas_trabalhadas['pin']=='4551']


#%%
df
days_with_four_records = df[df['pin'] == '4551'].groupby('date').filter(lambda x: len(x) == 4)['date'].nunique()
print(f"Number of days with 4 time records for pin 4551: {days_with_four_records}")











# %%
usuario_1= df[(df['pin']=='4551') & (df['date']=='01-04-2024')]
# %%
usuario_1['time'].sort_values()
times = usuario_1['time'].sort_values().values
total_time = 0

for i in range(len(times) - 1, 0, -1):
    time_diff = pd.to_datetime(times[i]) - pd.to_datetime(times[i - 1])
    total_time += time_diff.total_seconds()

total_time_hours = total_time // 3600
total_time_minutes = (total_time % 3600) // 60
total_time_seconds = total_time % 60

total_time_formatted = f"{int(total_time_hours)}h {int(total_time_minutes)}m {int(total_time_seconds)}s"
total_time_formatted
# %%
