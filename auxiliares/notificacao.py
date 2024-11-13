import pandas as pd
import sqlite3
import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Verificador para /data/bergamoto.db
def verificar_registros():
    db_path = '/home/br4b0/Desktop/novo_lar/bergamoto/data/bergamoto.db'
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

# Function to plot the data for a specific date
def plot_data(date):
    df = df_usuarios[df_usuarios['date'] == date]
    plt.figure(figsize=(10, 6))
    sns.barplot(x='name', y='registros', data=df)
    plt.title(f'Registros por Usuário em {date}')
    plt.xlabel('Nome')
    plt.ylabel('Registros')
    plt.ylim(0, 4)
    plt.yticks(range(0, 5, 1))
    st.pyplot(plt)

# Streamlit app
st.title('Registros por Usuário')
selected_date = st.selectbox('Selecione a Data:', df_usuarios['date'].unique())
plot_data(selected_date)