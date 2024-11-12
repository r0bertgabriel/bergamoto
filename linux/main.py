import datetime
import sqlite3
import cv2
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import signal
import io
import time
import threading
import csv
import os
from ttkthemes import ThemedTk

photo_window_open = False
lock = threading.Lock()

def create_table():
    # Define o caminho do banco de dados
    db_path = os.path.join('/home/br4b0/Desktop/novo_lar/bergamoto/data', 'bergamoto.db')
    # Verifica se o diretório do banco de dados existe, se não, cria o diretório
    if not os.path.exists('/home/br4b0/Desktop/novo_lar/bergamoto/data'):
        os.makedirs('/home/br4b0/Desktop/novo_lar/bergamoto/data')
    # Conecta ao banco de dados
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Cria a tabela 'horarios' se ela não existir
    c.execute('''CREATE TABLE IF NOT EXISTS horarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  pin TEXT, 
                  date TEXT,
                  time TEXT,
                  photo BLOB,
                  setor TEXT,
                  supervisor TEXT)''')
    conn.commit()
    conn.close()

def insert_record(name, pin, timestamp, photo_blob, setor, supervisor):
    date = timestamp.strftime("%d-%m-%Y")
    time = timestamp.strftime("%H:%M:00")
    db_path = os.path.join('/home/br4b0/Desktop/novo_lar/bergamoto/data', 'bergamoto.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Verifica o número de registros para o usuário na data atual
    c.execute("SELECT COUNT(*) FROM horarios WHERE pin = ? AND date = ?", (pin, date))
    record_count = c.fetchone()[0]
    
    if record_count >= 4:
        messagebox.showwarning("Limite Atingido".encode('utf-8'), "Você já fez 4 registros hoje.".encode('utf-8'))
        conn.close()
        return False

    # Insere um novo registro na tabela 'horarios'
    c.execute("INSERT INTO horarios (name, pin, date, time, photo, setor, supervisor) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (name, pin, date, time, photo_blob, setor, supervisor))
    conn.commit()
    conn.close()
    return True

def capture_photo():
    global photo_window_open
    img_blob = None

    def take_photo():
        nonlocal img_blob
        ret, frame = cam.read()
        if ret:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            with io.BytesIO() as output:
                img.save(output, format="PNG")
                img_blob = output.getvalue()
            messagebox.showinfo("Captura de Foto".encode('utf-8'), "Foto capturada".encode('utf-8'))
            cam.release()
            cv2.destroyAllWindows()
            root.quit()
        else:
            messagebox.showerror("Erro".encode('utf-8'), "Falha ao capturar a imagem".encode('utf-8'))

    def show_frame():
        if not cam.isOpened() or not root.winfo_exists():
            return
        ret, frame = cam.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
        if root.winfo_exists():
            lmain.after(10, show_frame)

    cam = cv2.VideoCapture(0)
    root = ThemedTk(theme="equilux")
    root.title("Captura de Foto")
    root.attributes("-topmost", True)
    root.attributes("-fullscreen", True)  # Define a janela para tela cheia

    style = ttk.Style(root)
    style.theme_use('equilux')

    frame = ttk.Frame(root, padding="10")
    frame.pack(expand=True, fill=tk.BOTH)

    lmain = ttk.Label(frame)
    lmain.pack(expand=True)

    capture_button = ttk.Button(frame, text="Capturar Foto", command=take_photo)
    capture_button.pack(pady=10)

    root.bind('<Return>', take_photo)  # Vincula a tecla Enter à função take_photo

    photo_window_open = True
    show_frame()
    
    # Tira a foto automaticamente após 3 segundos
    root.after(3000, take_photo)
    
    root.mainloop()
    cam.release()
    cv2.destroyAllWindows()
    root.destroy()
    photo_window_open = False
    return img_blob

class Employee:
    def __init__(self, name, pin, setor, supervisor):
        self.name = name
        self.pin = pin
        self.setor = setor
        self.supervisor = supervisor
        self.records = []

    def clock_in(self):
        now = datetime.datetime.now()
        photo_blob = capture_photo()
        if photo_blob:
            if insert_record(self.name, self.pin, now, photo_blob, self.setor, self.supervisor):
                self.records.append(now)
                self.analyze_records()
                time.sleep(1)

    def analyze_records(self):
        if len(self.records) == 2:
            pass
        elif len(self.records) == 3:
            pass
        elif len(self.records) == 4:
            pass
        else:
            pass

def main():
    create_table()
    employees = {}

    csv_path = 'data/people.csv'
    if not os.path.exists(csv_path):
        print(f"Arquivo {csv_path} não encontrado.".encode('utf-8'))
        return

    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pin = row['pin']
            name = row['name']
            setor = row['setor']
            supervisor = row['supervisor']
            employees[pin] = Employee(name, pin, setor, supervisor)

    def signal_handler():
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    def get_pin():
        global photo_window_open
        pin = None

        def submit_pin():
            nonlocal pin
            pin = pin_entry.get().strip()
            root.quit()

        with lock:
            while photo_window_open:
                time.sleep(0.1)

            root = ThemedTk(theme="equilux")
            root.title("Entrada de PIN")
            root.attributes("-topmost", True)
            root.attributes("-fullscreen", True)  # Define a janela para tela cheia

            style = ttk.Style(root)
            style.theme_use('equilux')

            frame = ttk.Frame(root, padding="10")
            frame.pack(expand=True, fill=tk.BOTH)

            label = ttk.Label(frame, text="Digite seu PIN:".encode('utf-8'), font=("Helvetica", 16))
            label.pack(pady=10)

            pin_entry = ttk.Entry(frame, font=("Helvetica", 16), justify='center')
            pin_entry.pack(pady=10)
            pin_entry.focus_set()  # Define o foco para o widget de entrada

            submit_button = ttk.Button(frame, text="Enviar".encode('utf-8'), command=submit_pin)
            submit_button.pack(pady=10)

            root.bind('<Return>', lambda event: submit_pin())  # Vincula a tecla Enter à função submit_pin

            root.mainloop()
            root.destroy()
        return pin

    def confirm_employee(employee):
        confirmed = False

        def confirm():
            nonlocal confirmed
            confirmed = True
            root.quit()

        def cancel():
            root.quit()

        with lock:
            root = ThemedTk(theme="equilux")
            root.title("Confirmação de Funcionário")
            root.attributes("-topmost", True)
            root.attributes("-fullscreen", True)  # Define a janela para tela cheia

            style = ttk.Style(root)
            style.theme_use('equilux')

            frame = ttk.Frame(root, padding="10")
            frame.pack(expand=True, fill=tk.BOTH)

            label = ttk.Label(frame, text=f"Nome: {employee.name}, Setor: {employee.setor}. É você?".encode('utf-8'), font=("Helvetica", 16))
            label.pack(pady=10)

            button_frame = ttk.Frame(frame)
            button_frame.pack(pady=10)

            confirm_button = ttk.Button(button_frame, text="Sim".encode('utf-8'), command=confirm)
            confirm_button.pack(side=tk.LEFT, padx=20)

            cancel_button = ttk.Button(button_frame, text="Não".encode('utf-8'), command=cancel)
            cancel_button.pack(side=tk.RIGHT, padx=20)

            root.bind('<Return>', lambda event: confirm())  # Vincula a tecla Enter à função confirm
            confirm_button.bind('<Return>', lambda event: confirm())  # Garante que a tecla Enter funcione no botão de confirmação

            root.mainloop()
            root.destroy()
        return confirmed

    while True:
        pin = get_pin()
        if pin == '----':
            print("Encerrando o programa.".encode('utf-8'))
            break
        if pin in employees:
            employee = employees[pin]
            if confirm_employee(employee):
                employee.clock_in()
                time.sleep(5)  # Aguarda a captura da foto e a inserção do registro serem concluídas
            else:
                messagebox.showerror("Erro".encode('utf-8'), "Confirmação falhou. Tente novamente.".encode('utf-8'))
        else:
            messagebox.showerror("Erro".encode('utf-8'), "PIN incorreto. Tente novamente.".encode('utf-8'))

if __name__ == "__main__":
    main()
