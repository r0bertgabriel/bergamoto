#%% USAR NO JUPYTER
from math import e
import re
import pandas as pd
import sqlite3
#%%
db_path = '/home/br4b0/Desktop/foss/DevcolabBR/bergamoto/data/bergamoto.db'
conn = sqlite3.connect(db_path)
query = """
SELECT pin, name, setor, date, time, COUNT(*) OVER (PARTITION BY pin, date) as registros
FROM horarios
"""

# %%
df = pd.read_sql_query(query, conn)


df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time

entrada = df[(df['registros'] == 1) & (df['time'] >= pd.to_datetime('07:00:00').time()) & 
             (df['time'] <= pd.to_datetime('11:00:00').time())]


# Ordena os horários em ordem crescente
df = df.sort_values(by=['pin', 'date', 'time'])

# Filtra os registros com duas entradas (visualização)
#%%
registro1 = df[df['registros'] == 1]
registro1
#%%
registro2 = df[df['registros'] == 2] #resolvido
registro2
#%%
registro3 = df[df['registros'] == 3]
registro3
#%%
registro4 = df[df['registros'] == 4]
registro4

#%%
# Cria um novo DataFrame para armazenar os horários de entrada e saída
result = pd.DataFrame(columns=['pin', 'name', 'setor', 'entrada', 'saida'])
# PARA 2 REGISTROS
rows = []
for pin, group in registro2.groupby(['pin', 'date']):
    if len(group) == 2:
        entrada = group.iloc[0]['time']
        saida = group.iloc[1]['time']
        if entrada < saida:
            rows.append({
                'pin': group.iloc[0]['pin'],
                'name': group.iloc[0]['name'],
                'setor': group.iloc[0]['setor'],
                'entrada': entrada,
                'saida': saida
            })

result = pd.concat([result, pd.DataFrame(rows)], ignore_index=True)

result



#%%
##### PARA 3 REGISTROS
result = pd.DataFrame(columns=['pin', 'name', 'setor', 'entrada', 'investigar', 'saida'])

rows = []
for pin, group in registro3.groupby(['pin', 'date']):
    if len(group) == 3:
        entrada = group.iloc[0]['time']
        investigar = group.iloc[1]['time']
        saida = group.iloc[2]['time']
        # Verifica se os horários estão dentro do intervalo permitido
        if pd.to_datetime('07:00:00').time() <= entrada <= pd.to_datetime('10:00:00').time():
            if pd.to_datetime('10:00:01').time() <= investigar <= pd.to_datetime('17:00:00').time():
                if saida > pd.to_datetime('17:00:00').time():
                    rows.append({
                        'pin': group.iloc[0]['pin'],
                        'name': group.iloc[0]['name'],
                        'setor': group.iloc[0]['setor'],
                        'entrada': entrada,
                        'investigar': investigar,
                        'saida': saida
                    })

result = pd.concat([result, pd.DataFrame(rows)], ignore_index=True)

result






# %%

conn.close()