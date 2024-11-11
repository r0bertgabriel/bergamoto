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
CREATE TABLE IF NOT EXISTS horarios (
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

# Função para gerar um horário aleatório dentro dos horários especificados
def generate_time(base_hour, variance):
    hour = random.randint(base_hour - variance, base_hour + variance)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{hour:02}:{minute:02}:{second:02}"

# Função para gerar um setor aleatório
def generate_setor():
    setores = ["vendas", "ti", "adm", "financeiro"]
    return random.choice(setores)

# Gerar dados para 20 funcionários
existing_pins = set()
start_date = datetime(2024, 4, 1)

# Gerar nomes e PINs para os funcionários
employees = [(generate_name(), generate_pin(existing_pins), generate_setor()) for _ in range(20)]

# Inserir dados por dia
for days_passed in range(61):  # 61 days from April 1 to May 31
    date = generate_date(start_date, days_passed)
    
    for name, pin, setor in employees:
        # 92% chance to have 4 records per day
        if random.random() < 0.92:
            times = [
                generate_time(8, 1),  # 8 AM ± 1 hour
                generate_time(12, 1), # 12 PM ± 1 hour
                generate_time(14, 1), # 2 PM ± 1 hour
                generate_time(20, 1)  # 8 PM ± 1 hour
            ]
        else:
            # Insert 1 to 3 records for the remaining 8% of the days
            num_records = random.randint(1, 3)
            times = sorted([generate_time(8, 1) for _ in range(num_records)])
        
        for time in times:
            cursor.execute('''
            INSERT INTO employees (name, pin, date, time, setor)
            VALUES (?, ?, ?, ?, ?)
            ''', (name, pin, date, time, setor))

# Salvar as mudanças e fechar a conexão
conn.commit()
conn.close()
