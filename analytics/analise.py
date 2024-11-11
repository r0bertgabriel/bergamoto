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
# %%
df
# %%
