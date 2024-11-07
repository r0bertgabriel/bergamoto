import datetime
import sqlite3
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import signal
import io
import time
import threading
import csv
import os

photo_window_open = False

def create_table():
    db_path = os.path.join('C:\\bergamoto\\data', 'horarios.db')
    if not os.path.exists('C:\\bergamoto\\data'):
        os.makedirs('C:\\bergamoto\\data')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
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
    db_path = os.path.join('C:\\bergamoto\\data', 'horarios.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check the number of records for the user on the current date
    c.execute("SELECT COUNT(*) FROM horarios WHERE pin = ? AND date = ?", (pin, date))
    record_count = c.fetchone()[0]
    
    if record_count >= 4:
        messagebox.showwarning("Limite Atingido", "Você já fez 4 registros hoje.")
        conn.close()
        return False

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
            messagebox.showinfo("Captura de Foto", "Foto capturada")
            cam.release()
            cv2.destroyAllWindows()
            root.quit()
        else:
            messagebox.showerror("Erro", "Falha ao capturar a imagem")

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
    root = tk.Tk()
    root.title("Captura de Foto")
    root.attributes("-topmost", True)

    frame = tk.Frame(root)
    frame.pack()

    lmain = tk.Label(frame)
    lmain.pack()

    capture_button = tk.Button(frame, text="Capturar Foto", command=take_photo)
    capture_button.pack()

    photo_window_open = True
    show_frame()
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

    csv_path = 'C:\\bergamoto\\data\\people.csv'
    if not os.path.exists(csv_path):
        print(f"Arquivo {csv_path} não encontrado.")
        return

    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pin = row['pin']
            name = row['name']
            setor = row['setor']
            supervisor = row['supervisor']
            employees[pin] = Employee(name, pin, setor, supervisor)

    def signal_handler(sig, frame):
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    def get_pin():
        global photo_window_open
        pin = None

        def submit_pin():
            nonlocal pin
            pin = pin_entry.get().strip()
            root.quit()

        while photo_window_open:
            time.sleep(1)

        root = tk.Tk()
        root.title("Entrada de PIN")
        root.geometry("400x200")
        root.attributes("-topmost", True)

        frame = tk.Frame(root)
        frame.pack(expand=True)

        label = tk.Label(frame, text="Digite seu PIN:", font=("Helvetica", 16))
        label.pack(pady=10)

        pin_entry = tk.Entry(frame, font=("Helvetica", 16), justify='center')
        pin_entry.pack(pady=10)

        submit_button = tk.Button(frame, text="Enviar", command=submit_pin, font=("Helvetica", 16))
        submit_button.pack(pady=10)

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

        root = tk.Tk()
        root.title("Confirmação de Funcionário")
        root.geometry("400x200")
        root.attributes("-topmost", True)

        frame = tk.Frame(root)
        frame.pack(expand=True)

        label = tk.Label(frame, text=f"Nome: {employee.name}, Setor: {employee.setor}. É você?", font=("Helvetica", 16))
        label.pack(pady=10)

        confirm_button = tk.Button(frame, text="Sim", command=confirm, font=("Helvetica", 16))
        confirm_button.pack(side=tk.LEFT, padx=20, pady=10)

        cancel_button = tk.Button(frame, text="Não", command=cancel, font=("Helvetica", 16))
        cancel_button.pack(side=tk.RIGHT, padx=20, pady=10)

        root.mainloop()
        root.destroy()
        return confirmed

    while True:
        pin = get_pin()
        if pin == '----':
            print("Encerrando o programa.")
            break
        if pin in employees:
            employee = employees[pin]
            if confirm_employee(employee):
                threading.Thread(target=employee.clock_in).start()
                time.sleep(3)
            else:
                messagebox.showerror("Erro", "Confirmação falhou. Tente novamente.")
        else:
            messagebox.showerror("Erro", "PIN incorreto. Tente novamente.")

if __name__ == "__main__":
    main()
