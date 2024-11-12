#%%
import pandas as pd
import sqlite3
import os
#%%
# Verificador para /data/bergamoto.db
def verificar_registros():
    db_path = '../data/bergamoto.db'
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
#%%

#%%
for data in df_usuarios['date'].unique():
    df = df_usuarios[df_usuarios['date'] == data]
    print(f"Data: {data}")
    for index, row in df.iterrows():
        print(f"Usuário: {row['name']} - Setor: {row['setor']} - Registros: {row['registros']}")
    print("\n")
# %%
