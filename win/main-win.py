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
                  photo BLOB)''')
    conn.commit()
    conn.close()

def insert_record(name, pin, timestamp, photo_blob):
    date = timestamp.strftime("%d-%m-%Y")
    time = timestamp.strftime("%H:%M:00")
    db_path = os.path.join('C:\\bergamoto\\data', 'horarios.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO horarios (name, pin, date, time, photo) VALUES (?, ?, ?, ?, ?)", (name, pin, date, time, photo_blob))
    conn.commit()
    conn.close()

def capture_photo():
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

    show_frame()
    root.mainloop()
    cam.release()
    cv2.destroyAllWindows()
    root.destroy()
    return img_blob

class Employee:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.records = []

    def clock_in(self):
        now = datetime.datetime.now()
        today_records = [record for record in self.records if record.date() == now.date()]
        if len(today_records) >= 4:
            messagebox.showwarning("Limite Atingido", "Você já fez 4 registros hoje.")
            return

        self.records.append(now)
        photo_blob = capture_photo()
        insert_record(self.name, self.pin, now, photo_blob)
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
            employees[pin] = Employee(name, pin)

    def signal_handler():
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        pin = input("Digite seu PIN: ")
        if pin in employees:
            employee = employees[pin]
            threading.Thread(target=employee.clock_in).start()
            time.sleep(3)
        else:
            print("PIN incorreto. Tente novamente.")

if __name__ == "__main__":
    main()