#%% USAR NO JUPYTER
import pandas as pd
import sqlite3
# import seaborn as sns
import matplotlib.pyplot as plt
#%%
db_path = '/home/br4b0/Desktop/foss/DevcolabBR/bergamoto/data/bergamoto.db'
conn = sqlite3.connect(db_path)
query = """
SELECT pin, name, setor, date, time, COUNT(*) OVER (PARTITION BY pin, date) as registros
FROM horarios
"""


# %%
df = pd.read_sql_query(query, conn)

# teste
"""
df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time

entrada = df[(df['registros'] == 1) & (df['time'] >= pd.to_datetime('07:00:00').time()) & 
             (df['time'] <= pd.to_datetime('11:00:00').time())]"""


# %% QUEM FALTOU:

query_usuarios = "SELECT pin, name, setor FROM usuarios"
df_usuarios = pd.read_sql_query(query_usuarios, conn)
df_usuarios

#%%
# Verifica quem faltou
# Converte a coluna 'date' para o tipo datetime para facilitar a comparação
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
df_usuarios['key'] = 1
unique_dates = pd.DataFrame(df['date'].unique(), columns=['date'])
unique_dates['key'] = 1

# Cria um DataFrame com todas as combinações possíveis de Colaboradores e datas
all_combinations = pd.merge(df_usuarios, unique_dates, on='key').drop('key', axis=1)

# Faz um merge com o DataFrame original para encontrar as combinações que não existem
merged = pd.merge(all_combinations, df[['pin', 'date']], on=['pin', 'date'], how='left', indicator=True)
df_faltaram = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)
df_faltaram.rename(columns={'date': 'dia-falta'}, inplace=True)
df_faltaram
#%%
#ANALISE DAS FALTAS

# Conta o número de faltas por usuário
faltas_por_usuario = df_faltaram['pin'].value_counts().reset_index()
faltas_por_usuario.columns = ['pin', 'faltas']

# Faz o merge para obter os nomes dos Colaboradores
faltas_por_usuario = faltas_por_usuario.merge(df_usuarios[['pin', 'name']], on='pin')

# Plota o gráfico
plt.figure(figsize=(10, 6))
plt.bar(faltas_por_usuario['name'], faltas_por_usuario['faltas'], color='skyblue')
plt.xlabel('Usuário')
plt.ylabel('Número de Faltas')
plt.title('Colaboradores que Mais Faltaram')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#%%
# Conta o número de faltas por usuário e por mês
df_faltaram['mes'] = df_faltaram['dia-falta'].dt.month
faltas_por_usuario_mes = df_faltaram.groupby(['pin', 'mes']).size().reset_index(name='faltas')

# Faz o merge para obter os nomes dos Colaboradores
faltas_por_usuario_mes = faltas_por_usuario_mes.merge(df_usuarios[['pin', 'name']], on='pin')

# Seleciona os 10 Colaboradores que mais faltaram
top_10_faltas = faltas_por_usuario.nlargest(10, 'faltas')['pin']
faltas_top_10 = faltas_por_usuario_mes[faltas_por_usuario_mes['pin'].isin(top_10_faltas)]

# Exibe o número de faltas de cada usuário por mês
for pin in top_10_faltas:
    user_data = faltas_top_10[faltas_top_10['pin'] == pin]
    print(f"Usuário: {user_data['name'].iloc[0]}")
    for mes in user_data['mes'].unique():
        faltas_mes = user_data[user_data['mes'] == mes]['faltas'].values[0]
        print(f"  Mês {mes}: {faltas_mes} faltas")
    print()

# Plota um gráfico de barras empilhadas para visualizar o número de faltas por mês para os 10 Colaboradores que mais faltaram
plt.figure(figsize=(12, 8))
faltas_top_10['mes_nome'] = faltas_top_10['mes'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%b'))
faltas_pivot = faltas_top_10.pivot(index='name', columns='mes_nome', values='faltas').fillna(0)
faltas_pivot = faltas_pivot[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]

# Ordena os Colaboradores pelo total de faltas no ano
faltas_pivot['total_faltas'] = faltas_pivot.sum(axis=1)
faltas_pivot = faltas_pivot.sort_values(by='total_faltas', ascending=False).drop(columns='total_faltas')

ax = faltas_pivot.plot(kind='bar', stacked=True, colormap='tab20', figsize=(12, 8))

# Adiciona os números de faltas dentro das barras
for container in ax.containers:
    ax.bar_label(container, label_type='center')

plt.xlabel('Colaboradores')
plt.ylabel('Número de Faltas totais no mês')
plt.title('Número de Faltas por Mês para os que Mais Faltaram')
plt.legend(title='Mês', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#%%

#%%
# Ordena os horários em ordem crescente
df = df.sort_values(by=['pin', 'date', 'time'])


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

#%%





# %%

conn.close()