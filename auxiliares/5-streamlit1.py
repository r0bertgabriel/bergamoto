#%%
import pandas as pd
import sqlite3
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Verificador para /data/bergamoto.db
def verificar_registros():
    db_path = '/home/br4b0/Desktop/foss/DevcolabBR/bergamoto/data/bergamoto.db'
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"O banco de dados {db_path} não foi encontrado.")
    
    conn = sqlite3.connect(db_path)
    query = """
    SELECT pin, name, setor, date, COUNT(*) as registros
    FROM horarios
    GROUP BY pin, date
    HAVING registros < 4
    """
    try:
        df = pd.read_sql_query(query, conn)
    except pd.io.sql.DatabaseError as e:
        raise ValueError("Erro ao executar a consulta SQL. Verifique se a tabela 'users' existe.") from e
    finally:
        conn.close()
    return df


#%%
# Chama a função e armazena o resultado em um DataFrame
df_usuarios = verificar_registros()

result = {}

for data in df_usuarios['date'].unique():
    df = df_usuarios[df_usuarios['date'] == data]
    result[data] = []
    for index, row in df.iterrows():
        result[data].append({
            "Usuário": row['name'],
            "Setor": row['setor'],
            "Registros": row['registros']
        })

# Save the result to a JSON file
with open('result.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

# Function to plot the data for a specific date and filter
def plot_data(date, filter_type, filter_value):
    if filter_type == 'Setor':
        df = df_usuarios[(df_usuarios['date'] == date) & (df_usuarios['setor'] == filter_value)]
    elif filter_type == 'Colaborador':
        df = df_usuarios[(df_usuarios['date'] == date) & (df_usuarios['name'] == filter_value)]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='name', y='registros', data=df)
    plt.title(f'Registros por Usuário em {date} - {filter_value}')
    plt.xlabel('Nome')
    plt.ylabel('Registros')
    plt.ylim(0, 4)
    plt.yticks(range(0, 5, 1))
    st.pyplot(plt)



def plot_horarios_faltantes(date, filter_type, filter_value):
    db_path = '/home/br4b0/Desktop/foss/DevcolabBR/bergamoto/data/bergamoto.db'
    conn = sqlite3.connect(db_path)
    query = """
   SELECT pin, name, setor, date, time, COUNT(*) as registros
    FROM horarios
    GROUP BY pin, date
    HAVING registros < 4 AND date = ? AND {} = ?
    
    """.format('setor' if filter_type == 'Setor' else 'name')
        
    df = pd.read_sql_query(query, conn, params=(date, filter_value))
    conn.close()
    
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce')  # Convert to datetime format
    df['time'] = df['time'].dt.strftime('%H:%M:%S')  # Convert to string format
    df = df.dropna(subset=['time'])  # Drop rows with invalid time values
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='name', y='time', data=df, hue='name', palette='tab10', s=100, legend=False)
    plt.title(f'Horários de Ponto em {date} - {filter_value}')
    plt.ylabel('Horário')
    plt.xlabel('Nome')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(nbins=10, prune='both'))
    plt.grid(True)
    st.pyplot(plt)

# Streamlit app
st.title('Análise de registros faltantes')

# Checkbox to select configuration
option = st.radio('Selecione a opção:', ['Quantidade de pontos batidos', 'Horários de ponto (para faltantes)'])
nova_config = option == 'Quantidade de pontos batidos'
horarios_pontos = option == 'Horários de ponto (para faltantes)'

if nova_config:
    selected_date = st.selectbox('Selecione a Data:', df_usuarios['date'].unique())
    filter_type = st.selectbox('Filtrar por:', ['Setor', 'Colaborador'])

    if filter_type == 'Setor':
        selected_filter = st.selectbox('Selecione o Setor:', df_usuarios['setor'].unique())
    elif filter_type == 'Colaborador':
        selected_filter = st.selectbox('Selecione o Colaborador:', df_usuarios['name'].unique())

    plot_data(selected_date, filter_type, selected_filter)
else:
    # Código da configuração anterior
    st.write("Usando a configuração anterior.")
    # Adicione aqui o código da configuração anterior, se necessário




if horarios_pontos:
    selected_date = st.selectbox('Selecione a Data:', df_usuarios['date'].unique())
    filter_type = st.selectbox('Filtrar por:', ['Setor', 'Colaborador'])

    if filter_type == 'Setor':
        selected_filter = st.selectbox('Selecione o Setor:', df_usuarios['setor'].unique())
    elif filter_type == 'Colaborador':
        selected_filter = st.selectbox('Selecione o Colaborador:', df_usuarios['name'].unique())

    plot_horarios_faltantes(selected_date, filter_type, selected_filter)