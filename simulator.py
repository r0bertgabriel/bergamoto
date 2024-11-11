import sqlite3
import random
import os
from datetime import datetime, timedelta

# Verificar se o diretório 'data' existe, caso contrário, criar
if not os.path.exists('data'):
    os.makedirs('data')

# Conectar ao banco de dados (o arquivo será criado se não existir)
conn = sqlite3.connect('data/bergamoto.db')
cursor = conn.cursor()

# Criar a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    pin TEXT,
    date TEXT,
    time TEXT,
    setor TEXT
)
''')

# Função para gerar um nome aleatório
def generate_name():
    first_names = ["Alice", "Bob", "Charlie", "David", "Eva"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Função para gerar um PIN único
def generate_pin(existing_pins):
    while True:
        pin = f"{random.randint(1000, 9999)}"
        if pin not in existing_pins:
            existing_pins.add(pin)
            return pin

# Função para gerar uma data crescente
def generate_date(start_date, days_passed):
    return (start_date + timedelta(days=days_passed)).strftime('%d-%m-%Y')

# Função para gerar um horário aleatório
def generate_time():
    return f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}"

# Função para gerar um setor aleatório
def generate_setor():
    setores = ["vendas", "ti", "adm", "financeiro"]
    return random.choice(setores)

# Gerar dados para 20 funcionários
existing_pins = set()
start_date = datetime(2024, 4, 1)
days_passed = 0

for _ in range(20):
    name = generate_name()
    pin = generate_pin(existing_pins)
    setor = generate_setor()
    
    for _ in range(61):  # 61 days from April 1 to May 31
        days_passed += 1
        date = generate_date(start_date, days_passed)
        
        # 90% chance to have 4 records per day
        if random.random() < 0.9:
            for _ in range(4):
                time = generate_time()
                cursor.execute('''
                INSERT INTO employees (name, pin, date, time, setor)
                VALUES (?, ?, ?, ?, ?)
                ''', (name, pin, date, time, setor))
        else:
            # Insert 1 to 3 records for the remaining 10% of the days
            for _ in range(random.randint(1, 3)):
                time = generate_time()
                cursor.execute('''
                INSERT INTO employees (name, pin, date, time, setor)
                VALUES (?, ?, ?, ?, ?)
                ''', (name, pin, date, time, setor))

# Salvar as mudanças e fechar a conexão
conn.commit()
conn.close()