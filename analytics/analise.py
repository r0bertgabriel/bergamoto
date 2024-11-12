#%%
import pandas as pd
import os
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
