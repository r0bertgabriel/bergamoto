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
df['entrada'] = df.groupby('name').cumcount() == 0
df['s-almoco'] = df.groupby('name').cumcount() == 1
df['r-almoco'] = df.groupby('name').cumcount() == 2
df['saida'] = df.groupby('name').cumcount() == 3

df['entrada'] = df['entrada'].astype(bool)
df['s-almoco'] = df['s-almoco'].astype(bool)
df['r-almoco'] = df['r-almoco'].astype(bool)
df['saida'] = df['saida'].astype(bool)
# %%
df
# %%
